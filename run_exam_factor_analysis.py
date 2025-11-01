#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_exam_factor_analysis.py

End-to-end pipeline:
- Load transposed Excel (rows=students; first column 'student_id').
- First row must be 'test_student_sp24_fe' with per-item maxima.
- Normalize → Z-score → Scree plot → Factor Analysis (no rotation).
- Save outputs (Excel + PNG).

Usage:
python run_exam_factor_analysis.py --input path/to/file.xlsx --output_dir outputs
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from scipy.stats import zscore
from sklearn.decomposition import FactorAnalysis

def _colwise_corr(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    A = (A - A.mean(axis=0)) / (A.std(axis=0, ddof=0) + 1e-12)
    B = (B - B.mean(axis=0)) / (B.std(axis=0, ddof=0) + 1e-12)
    return (A.T @ B) / A.shape[0]

def run_pipeline(input_path: str, output_dir: str) -> None:
    ipath = Path(input_path)
    odir = Path(output_dir)
    odir.mkdir(parents=True, exist_ok=True)

    print(f"Loading: {ipath}")
    df = pd.read_excel(ipath)

    if "student_id" not in df.columns:
        raise ValueError("Missing 'student_id' column.")
    if not (df["student_id"] == "test_student_sp24_fe").any():
        raise ValueError("Missing 'test_student_sp24_fe' row for per-item maxima.")

    max_scores = df.loc[df["student_id"] == "test_student_sp24_fe"].iloc[0, 1:]
    data = df.loc[df["student_id"] != "test_student_sp24_fe"].reset_index(drop=True)

    df_norm = data.copy()
    for col in df_norm.columns[1:]:
        df_norm[col] = pd.to_numeric(df_norm[col], errors="coerce")
        max_scores[col] = pd.to_numeric(max_scores[col], errors="coerce")
        df_norm[col] = df_norm[col] / max_scores[col]

    df_z = df_norm.copy()
    for col in df_z.columns[1:]:
        df_z[col] = zscore(df_norm[col].astype(float), nan_policy="omit")

    norm_path = odir / "students_normalized_zscored.xlsx"
    with pd.ExcelWriter(norm_path, engine="openpyxl") as w:
        df_norm.to_excel(w, index=False, sheet_name="normalized")
        df_z.to_excel(w, index=False, sheet_name="z_scored")
    print(f"Saved normalized + z-scored to: {norm_path}")

    X = df_z.drop(columns=["student_id"]).apply(pd.to_numeric, errors="coerce")
    X = X.fillna(X.mean(axis=0))
    X = (X - X.mean(axis=0)) / X.std(axis=0, ddof=0)
    X = X.replace([np.inf, -np.inf], np.nan).fillna(0.0)

    corr = np.corrcoef(X.T)
    eigvals, _ = np.linalg.eig(corr)
    eigvals = np.sort(np.real(eigvals))[::-1]

    plt.figure()
    plt.plot(range(1, len(eigvals) + 1), eigvals, marker="o")
    plt.axhline(y=1.0, color="r", linestyle="--")
    plt.title("Scree Plot (Eigenvalues)")
    plt.xlabel("Factor"); plt.ylabel("Eigenvalue")
    plt.grid(True, linestyle="--", linewidth=0.5)
    scree_path = odir / "scree_plot.png"
    plt.savefig(scree_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved scree plot to: {scree_path}")

    n_kaiser = int((eigvals > 1.0).sum())
    n_factors = max(2, min(8, n_kaiser if n_kaiser > 0 else 2))
    print(f"Eigenvalues > 1: {n_kaiser}  →  using n_factors = {n_factors}")

    fa = FactorAnalysis(n_components=n_factors, random_state=0)
    Z_scores = fa.fit_transform(X.values)

    loadings = _colwise_corr(X.values, Z_scores)
    factor_cols = [f"Factor{j+1}" for j in range(n_factors)]
    load_df = pd.DataFrame(loadings, index=X.columns, columns=factor_cols)

    items = load_df.reset_index().rename(columns={"index": "question_id"})
    items["TopFactor"] = items[factor_cols].abs().idxmax(axis=1)
    items["LoadingStrength"] = items.apply(lambda r: r[r["TopFactor"]], axis=1)

    fa_out = odir / "FA_outputs_simple.xlsx"
    with pd.ExcelWriter(fa_out, engine="openpyxl") as w:
        pd.DataFrame(Z_scores, columns=factor_cols).to_excel(w, index=False, sheet_name="student_factor_scores")
        load_df.to_excel(w, sheet_name="item_loadings")
        items.to_excel(w, index=False, sheet_name="items_topfactor")
    print(f"Saved FA outputs to: {fa_out}")
    print("Done.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Normalize → Z-score → Scree → Factor Analysis")
    ap.add_argument("--input", required=True, help="Path to transposed Excel file")
    ap.add_argument("--output_dir", default="outputs", help="Directory for outputs (default: outputs)")
    args = ap.parse_args()
    run_pipeline(args.input, args.output_dir)
