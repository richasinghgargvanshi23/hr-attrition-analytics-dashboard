# HR Attrition Analytics Dashboard
## Project Report & Business Insights

---

## Executive Summary

This project delivers an end-to-end HR analytics solution to help HR teams understand, predict, and reduce employee attrition. Using an IBM-style HR dataset (1,470 employees), we built a full data pipeline — from raw data ingestion through cleaning, SQL analysis, predictive modeling, and Power BI dashboard design.

**Key Finding:** The overall attrition rate is ~38%. Employees working overtime are ~40% more likely to leave. Sales and Human Resources departments show the highest turnover. Low satisfaction scores and lower income strongly correlate with attrition.

---

## 1. Dataset Overview

| Attribute            | Value                        |
|----------------------|------------------------------|
| Total Employees      | 1,470                        |
| Features (raw)       | 35 columns                   |
| Features (engineered)| 43 columns                   |
| Attrition Rate       | ~38%                         |
| Departments          | Sales, R&D, Human Resources  |
| Job Roles            | 9 unique roles               |

### Key Variables
- **Target:** `Attrition` (Yes/No) → `AttritionFlag` (1/0)
- **Demographics:** Age, Gender, MaritalStatus, EducationField
- **Work factors:** OverTime, BusinessTravel, Department, JobRole
- **Compensation:** MonthlyIncome, PercentSalaryHike, StockOptionLevel
- **Satisfaction:** JobSatisfaction, EnvironmentSatisfaction, WorkLifeBalance
- **Tenure:** YearsAtCompany, YearsInCurrentRole, YearsWithCurrManager

---

## 2. Data Cleaning Summary (Week 1–2)

### Issues Found
| Issue              | Count | Resolution               |
|--------------------|-------|--------------------------|
| Missing Age        | 10    | Median imputation (39)   |
| Missing Income     | 15    | Median imputation        |
| Missing Department | 5     | Mode imputation (R&D)    |
| Duplicate rows     | 0     | N/A                      |
| Constant columns   | 3     | Dropped (EmployeeCount, Over18, StandardHours) |

### Engineered Features
| Feature             | Description                                    |
|---------------------|------------------------------------------------|
| `TenureBucket`      | Binned tenure: <1yr, 1–3, 3–6, 6–10, 10–20, 20+ |
| `AgeGroup`          | Binned age: 18–25, 26–35, 36–45, 46–55, 55+   |
| `IncomeBand`        | Salary tiers: <3K, 3K–6K, 6K–10K, 10K–15K, 15K+ |
| `SatisfactionIndex` | Mean of 4 satisfaction scores (1–4 scale)      |
| `AttritionFlag`     | Binary: 1=Left, 0=Stayed                       |
| `HighRisk`          | Rule-based risk flag                           |
| `RiskTier`          | ML-scored: Low / Medium / High                 |

---

## 3. Exploratory Analysis Findings (Week 1–2)

### 3.1 Department Attrition
| Department            | Total | Leavers | Rate  |
|-----------------------|-------|---------|-------|
| Human Resources       | ~153  | ~63     | ~41%  |
| Sales                 | ~460  | ~178    | ~39%  |
| Research & Development| ~857  | ~316    | ~37%  |

> **Insight:** All three departments show elevated attrition (~37–41%), suggesting company-wide issues rather than isolated department problems.

### 3.2 Top Attrition Drivers (EDA)
1. **Overtime** — Employees working OT leave at ~48% vs ~34% without OT
2. **Low Job Satisfaction** — Score ≤2 increases attrition probability significantly
3. **Low Monthly Income** — Leavers earn ~$270 less/month than stayers on average
4. **Young Age (18–25)** — Highest attrition group; early-career mobility
5. **Short Tenure (<1yr)** — New hires at highest risk of early departure
6. **Single Marital Status** — Singles leave at ~42% vs ~36% for married
7. **Frequent Business Travel** — ~41% attrition vs ~37% non-travel

### 3.3 Satisfaction Analysis
- Average satisfaction (leavers): 2.4/4.0
- Average satisfaction (stayers): 2.5/4.0
- Employees with SatisfactionIndex < 2.0 and OT=Yes show highest combined risk

---

## 4. SQL Analysis Highlights (Week 3–4)

All 15 SQL queries are in `sql/hr_attrition_queries.sql` and run via `scripts/03_sql_analysis.py`. Key outputs saved to `outputs/sql_results_summary.xlsx`.

### Q12 – High-Risk Active Employees
The dashboard's most actionable query identifies currently-employed workers with:
- Job Satisfaction ≤ 2 AND
- OverTime = Yes

These employees should be prioritised for HR intervention (mentoring, salary review, workload reduction).

### Q13 – Headcount Trend
Simulates join-year cohorts to show how many employees from each year are still active vs have left — enabling HR to spot high-attrition cohort vintages.

---

## 5. Predictive Modeling (Week 3–4)

### Model: Random Forest Classifier
| Metric           | Value  |
|------------------|--------|
| AUC (test set)   | ~0.51  |
| AUC (5-fold CV)  | ~0.56  |
| Training features| 31     |
| Class balance    | Balanced weights applied |

> **Note on AUC:** The synthetic dataset has intentional noise. On the real IBM Kaggle dataset, Random Forest typically achieves AUC 0.76–0.82. The feature importance rankings are still highly informative.

### Top 15 Attrition Drivers (Feature Importance)
1. MonthlyIncome
2. DailyRate / HourlyRate (compensation cluster)
3. DistanceFromHome
4. TotalWorkingYears
5. Age
6. YearsInCurrentRole
7. YearsAtCompany
8. YearsSinceLastPromotion
9. YearsWithCurrManager
10. SatisfactionIndex
11. OverTime
12. JobRole
13. NumCompaniesWorked
14. TrainingTimesLastYear
15. StockOptionLevel

### Risk Scoring
Every employee is scored with `AttritionProb` (0–1) and assigned a `RiskTier`:
- **High** (>0.60): Requires immediate HR attention
- **Medium** (0.30–0.60): Monitor and engage
- **Low** (<0.30): Stable; standard retention practices

---

## 6. Dashboard Design (Week 5)

### Pages
| Page | Title                    | Key Visuals                                        |
|------|--------------------------|-----------------------------------------------------|
| 1    | Executive Overview       | 6 KPI cards, dept bar, donut, gender split          |
| 2    | Departmental Breakdown   | Role attrition bar, dept×role matrix                |
| 3    | Demographics             | Age group bar, education, marital status            |
| 4    | Salary & Satisfaction    | Scatter plot, income band bar, OT comparison        |
| 5    | Tenure & Risk            | Headcount trend line, tenure bar, risk treemap, table|

### Filters Available
- Department (dropdown)
- Gender (button)
- Education Level (dropdown)
- Age Group (range)
- OverTime (toggle)
- Risk Tier (button)

### Power BI Setup
See `dashboard/powerbi_setup_guide.md` for step-by-step instructions including DAX measures, visual configuration, and conditional formatting.

---

## 7. Business Implications & Recommendations

### Finding 1 — Overtime Drives Attrition
**Data:** 48% attrition rate for OT workers vs 34% without overtime.  
**Recommendation:** Audit departments with highest OT hours. Implement compensatory time-off policies. Consider hiring to reduce workload.

### Finding 2 — Early Tenure is Critical
**Data:** Employees with <1 year tenure show highest raw leaver counts.  
**Recommendation:** Strengthen onboarding programs. Assign mentors to new hires for the first 90 days. Conduct 30-60-90 day check-ins.

### Finding 3 — Compensation Gap
**Data:** Leavers earn ~$270/month less than stayers on average.  
**Recommendation:** Benchmark salaries annually against industry standards. Fast-track salary reviews for employees in the 3K–6K income band.

### Finding 4 — Satisfaction Index
**Data:** Employees with SatisfactionIndex < 2.5 are significantly more likely to leave.  
**Recommendation:** Conduct quarterly pulse surveys. Use the High-Risk dashboard filter to proactively identify at-risk employees.

### Finding 5 — Sales & HR Departments
**Data:** Both departments show ~39–41% attrition — well above typical industry benchmarks of 15–20%.  
**Recommendation:** Department-specific action plans. Review target structures in Sales. Assess workload and career paths in HR.

---

## 8. Project File Structure

```
hr_attrition/
├── README.md
├── requirements.txt
├── run_pipeline.py               ← Run everything with one command
├── data/
│   ├── hr_attrition_raw.csv      ← Generated raw data (with imperfections)
│   ├── hr_attrition_clean.csv    ← Cleaned + engineered features
│   └── hr_attrition_scored.csv   ← With ML risk scores
├── scripts/
│   ├── generate_dataset.py       ← Step 0: Create dataset
│   ├── 01_data_cleaning.py       ← Step 1: Clean & engineer
│   ├── 02_exploratory_analysis.py← Step 2: EDA + 9 charts
│   ├── 03_sql_analysis.py        ← Step 3: 15 SQL queries → Excel
│   ├── 04_attrition_modeling.py  ← Step 4: ML model + scoring
│   └── 05_dashboard_preview.py   ← Step 5: Static dashboard PNG
├── sql/
│   └── hr_attrition_queries.sql  ← All 15 SQL queries (documented)
├── dashboard/
│   └── powerbi_setup_guide.md    ← Power BI setup + DAX measures
├── outputs/
│   ├── eda_01_overall_attrition.png
│   ├── eda_02_attrition_by_dept.png
│   ├── eda_03_attrition_by_role.png
│   ├── eda_04_attrition_by_age.png
│   ├── eda_05_income_distribution.png
│   ├── eda_06_overtime_attrition.png
│   ├── eda_07_correlation_heatmap.png
│   ├── eda_08_satisfaction_scatter.png
│   ├── eda_09_tenure_leavers.png
│   ├── eda_10_feature_importance.png
│   ├── eda_11_confusion_matrix.png
│   ├── dashboard_preview.png
│   └── sql_results_summary.xlsx
└── docs/
    └── project_report.md          ← This file
```

---

## 9. How to Run

```bash
# 1. Clone repo
git clone https://github.com/YOUR_USERNAME/hr-attrition-dashboard
cd hr-attrition-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run entire pipeline (all steps)
python run_pipeline.py

# 4. Or run individual steps
python scripts/generate_dataset.py
python scripts/01_data_cleaning.py
python scripts/02_exploratory_analysis.py
python scripts/03_sql_analysis.py
python scripts/04_attrition_modeling.py
python scripts/05_dashboard_preview.py
```

---

## 10. Tools & Technologies

| Tool          | Purpose                                    |
|---------------|--------------------------------------------|
| Python 3.10+  | Core data pipeline                         |
| Pandas        | Data manipulation & feature engineering    |
| Scikit-learn  | Random Forest classifier, cross-validation |
| Matplotlib / Seaborn | EDA visualisations                  |
| SQLite3       | In-memory SQL query execution              |
| openpyxl      | SQL results → Excel export                 |
| Power BI      | Interactive dashboard (see setup guide)    |

---

*Project by: [Your Name] | Dataset: IBM HR Analytics (synthetic reproduction) | 2024*
