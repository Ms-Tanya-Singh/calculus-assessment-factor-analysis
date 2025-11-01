# Mock Data Guide

This folder contains **synthetic** exam data to demonstrate the pipeline without exposing any real student information.

## Files
- `mock_pretransposed.xlsx` — **Pre-transposed** format (each **row is an item**; each **column is a student**). It also includes a `max_points` column per item.
- `mock_transposed.xlsx` — **Transposed** format expected by the pipeline (each **row is a student**; first column `student_id`). The first row is a special label `test_student_sp24_fe` that stores the **per-item maximum points**.

## How the pipeline works (end-to-end)

1. **Start** from the **transposed** file (e.g., `mock_transposed.xlsx` or your real file) where rows are students and columns are items.
2. The pipeline:
   - Extracts the **max points** from the special row `test_student_sp24_fe`
   - **Normalizes** each item to a 0–1 scale using its max
   - **Z-scores** each item (center 0, std 1) so items are comparable
   - Computes a **scree plot** (eigenvalues of item correlation matrix)
   - Runs **linear factor analysis** (no rotation) and exports:
     - `student_factor_scores`
     - `item_loadings`
     - `items_topfactor` (which factor each item loads on most)
3. Outputs are written to the `outputs/` folder:
   - `students_normalized_zscored.xlsx`
   - `FA_outputs_simple.xlsx`
   - `scree_plot.png`

## To test the pipeline with mock data

```bash
# from the repo root
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run using the transposed mock file
python src/run_pipeline.py --input sample_data/mock_transposed.xlsx --output_dir outputs
```

