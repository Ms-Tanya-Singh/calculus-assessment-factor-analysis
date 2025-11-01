# Calculus Exam Factor Analysis

This repository demonstrates a reproducible pipeline for analyzing question-level performance on a Calculus final exam.  
The goal is to understand **what underlying skills** the exam measures — beyond a single total score — using **normalization, z-scoring, and factor analysis**.

---

##  Purpose

This project investigates:

- Whether the exam measures one broad “calculus proficiency” skill
- Whether sub-skills emerge (e.g., limits, differentiation, applications)
- How item-level performance clusters into latent dimensions

This supports **assessment validity**, fairness, and improvement in question design.

---

##  What the pipeline does

| Step | Method |
|----|----|
1 | Load student × question matrix (transposed format)  
2 | Extract maximum points per question (from `test_student_sp24_fe` row)  
3 | Normalize all item scores to 0–1  
4 | Standardize each item with z-scores  
5 | Compute item-correlation matrix  
6 | Generate a Scree Plot (Eigenvalues)  
7 | Apply Linear Factor Analysis (no rotation)  
8 | Export factor loadings & student factor scores  

---

## Scree Plot (Latent Structure)

> **Figure 1. Scree Plot of Exam Eigenvalues**  
> The first eigenvalue is dominant, indicating a **strong general calculus proficiency factor**.  
> An elbow appears around **2–3 factors**, suggesting **secondary skill dimensions** such as procedural fluency and conceptual understanding.  
> Factors above the red horizontal line (eigenvalue = 1) meet the **Kaiser criterion**, meaning they explain meaningful variance.

📎 *Upload your file here: `docs/scree_plot.png`*  
*(Place image in repo, it will display automatically)*

---

##  Interpretation

- The exam strongly measures an **overall calculus mastery construct**
- **Additional sub-skills** also influence performance, likely:
  - Conceptual reasoning  
  - Differentiation procedures  
  - Application modeling / problem-solving  

This structure aligns with modern views of mathematical cognition:  
> **a dominant general skill with multiple supporting abilities.**

---

##  Repository Structure

```
.
├── run_exam_factor_analysis.py   # Main analysis script
├── sample_data/                  # Synthetic example data
├── outputs/                      # Folder created by script
└── docs/
    └── scree_plot.png            # (Upload after running)
```

---

##  Running the Analysis

### Install deps
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Run on your dataset
```bash
python run_exam_factor_analysis.py   --input data/students_with_final_exam_score_transposed.xlsx   --output_dir outputs
```

### Run on mock sample data
```bash
python run_exam_factor_analysis.py   --input sample_data/mock_transposed.xlsx   --output_dir outputs
```

---

## Output Files

| File | Contents |
|---|---|
`students_normalized_zscored.xlsx` | normalized + z-scored responses  
`FA_outputs_simple.xlsx` | student factor scores, item loadings, top factor per item  
`scree_plot.png` | eigenvalue plot showing latent skill structure  

---

##  Educational Value

This project demonstrates:

- Assessment analytics for STEM courses  
- Intro psychometrics for classroom research  
- Transparent & reproducible evaluation of exam validity  
- Student-centered fairness in measurement  

---

## License

Open-academic / educational use encouraged.

---

### Questions? Improvements?

Happy to iterate — feedback welcome!

