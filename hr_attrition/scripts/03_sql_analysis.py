"""
03_sql_analysis.py
────────────────────────────────────────────────────────────────────────────
HR Attrition Project  –  SQL Analysis (SQLite runner)
────────────────────────────────────────────────────────────────────────────
Loads the clean CSV into an in-memory SQLite database and executes all
queries from sql/hr_attrition_queries.sql, printing results and saving
a summary Excel workbook.

Input  : data/hr_attrition_clean.csv
Output : outputs/sql_results_summary.xlsx
"""

import os
import sqlite3
import textwrap
import pandas as pd

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA     = os.path.join(BASE, "data", "hr_attrition_clean.csv")
OUT_XLSX = os.path.join(BASE, "outputs", "sql_results_summary.xlsx")
os.makedirs(os.path.join(BASE, "outputs"), exist_ok=True)

# ── Load data into SQLite ─────────────────────────────────────────────────────
print("=" * 60)
print("HR ATTRITION  –  SQL ANALYSIS")
print("=" * 60)
df = pd.read_csv(DATA)

# Convert categoricals so SQLite can store them
for col in df.select_dtypes(include="category").columns:
    df[col] = df[col].astype(str)

con = sqlite3.connect(":memory:")
df.to_sql("hr_attrition", con, if_exists="replace", index=False)
print(f"\n[DB]  Loaded {len(df)} rows into SQLite table 'hr_attrition'")

# ── Define queries ────────────────────────────────────────────────────────────
queries = {
    "Q1_Overall_Attrition": """
        SELECT Attrition,
               COUNT(*) AS Employees,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM hr_attrition), 2)
                   AS PctOfTotal
        FROM hr_attrition GROUP BY Attrition ORDER BY Employees DESC
    """,
    "Q2_By_Department": """
        SELECT Department, COUNT(*) AS Total,
               SUM(AttritionFlag) AS Leavers,
               ROUND(SUM(AttritionFlag)*100.0/COUNT(*),2) AS AttritionRate_pct
        FROM hr_attrition GROUP BY Department ORDER BY AttritionRate_pct DESC
    """,
    "Q3_By_JobRole": """
        SELECT JobRole, Department, COUNT(*) AS Total,
               SUM(AttritionFlag) AS Leavers,
               ROUND(SUM(AttritionFlag)*100.0/COUNT(*),2) AS AttritionRate_pct
        FROM hr_attrition GROUP BY JobRole, Department
        ORDER BY AttritionRate_pct DESC
    """,
    "Q4_By_AgeGroup": """
        SELECT AgeGroup, COUNT(*) AS Total,
               SUM(AttritionFlag) AS Leavers,
               ROUND(SUM(AttritionFlag)*100.0/COUNT(*),2) AS AttritionRate_pct
        FROM hr_attrition GROUP BY AgeGroup ORDER BY AgeGroup
    """,
    "Q5_Leavers_Raw": """
        SELECT EmployeeID, Age, Department, JobRole, MonthlyIncome,
               YearsAtCompany, JobSatisfaction, OverTime, MaritalStatus
        FROM hr_attrition WHERE Attrition='Yes' ORDER BY YearsAtCompany
    """,
    "Q6_Avg_Tenure_Income": """
        SELECT Attrition,
               ROUND(AVG(YearsAtCompany),2) AS AvgTenure_yrs,
               ROUND(AVG(MonthlyIncome),0)  AS AvgMonthlyIncome,
               ROUND(AVG(JobSatisfaction),2)AS AvgJobSatisfaction,
               ROUND(AVG(SatisfactionIndex),2) AS AvgSatisfactionIndex
        FROM hr_attrition GROUP BY Attrition
    """,
    "Q7_OverTime": """
        SELECT OverTime, COUNT(*) AS Total,
               SUM(AttritionFlag) AS Leavers,
               ROUND(SUM(AttritionFlag)*100.0/COUNT(*),2) AS AttritionRate_pct
        FROM hr_attrition GROUP BY OverTime
    """,
    "Q8_Tenure_Bucket": """
        SELECT TenureBucket, COUNT(*) AS Total,
               SUM(AttritionFlag) AS Leavers,
               ROUND(SUM(AttritionFlag)*100.0/COUNT(*),2) AS AttritionRate_pct
        FROM hr_attrition GROUP BY TenureBucket
    """,
    "Q9_Income_Band": """
        SELECT IncomeBand, COUNT(*) AS Total,
               SUM(AttritionFlag) AS Leavers,
               ROUND(SUM(AttritionFlag)*100.0/COUNT(*),2) AS AttritionRate_pct
        FROM hr_attrition GROUP BY IncomeBand
    """,
    "Q10_Gender": """
        SELECT Gender, COUNT(*) AS Total,
               SUM(AttritionFlag) AS Leavers,
               ROUND(SUM(AttritionFlag)*100.0/COUNT(*),2) AS AttritionRate_pct
        FROM hr_attrition GROUP BY Gender
    """,
    "Q11_Education": """
        SELECT Education_Label, Education, COUNT(*) AS Total,
               SUM(AttritionFlag) AS Leavers,
               ROUND(SUM(AttritionFlag)*100.0/COUNT(*),2) AS AttritionRate_pct
        FROM hr_attrition GROUP BY Education_Label, Education ORDER BY Education
    """,
    "Q12_HighRisk": """
        SELECT EmployeeID, Age, Department, JobRole, MonthlyIncome,
               YearsAtCompany, JobSatisfaction, EnvironmentSatisfaction,
               WorkLifeBalance, OverTime, SatisfactionIndex
        FROM hr_attrition
        WHERE Attrition='No' AND JobSatisfaction<=2 AND OverTime='Yes'
        ORDER BY SatisfactionIndex ASC LIMIT 10
    """,
    "Q13_Headcount_Trend": """
        SELECT (2024 - YearsAtCompany) AS JoinYear,
               COUNT(*) AS TotalJoined,
               SUM(AttritionFlag) AS TotalLeft,
               COUNT(*)-SUM(AttritionFlag) AS StillActive
        FROM hr_attrition GROUP BY JoinYear ORDER BY JoinYear
    """,
    "Q14_MaritalStatus": """
        SELECT MaritalStatus, COUNT(*) AS Total,
               SUM(AttritionFlag) AS Leavers,
               ROUND(SUM(AttritionFlag)*100.0/COUNT(*),2) AS AttritionRate_pct
        FROM hr_attrition GROUP BY MaritalStatus ORDER BY AttritionRate_pct DESC
    """,
    "Q15_BusinessTravel": """
        SELECT BusinessTravel, COUNT(*) AS Total,
               SUM(AttritionFlag) AS Leavers,
               ROUND(SUM(AttritionFlag)*100.0/COUNT(*),2) AS AttritionRate_pct
        FROM hr_attrition GROUP BY BusinessTravel ORDER BY AttritionRate_pct DESC
    """,
}

# ── Execute & display ─────────────────────────────────────────────────────────
results = {}
for name, sql in queries.items():
    res = pd.read_sql_query(textwrap.dedent(sql), con)
    results[name] = res
    print(f"\n{'─'*55}")
    print(f"  {name}")
    print(f"{'─'*55}")
    print(res.to_string(index=False))

con.close()

# ── Save to Excel (one sheet per query) ──────────────────────────────────────
with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as writer:
    for name, res in results.items():
        sheet = name[:31]          # Excel sheet name max 31 chars
        res.to_excel(writer, sheet_name=sheet, index=False)

print(f"\n{'='*60}")
print(f"[SAVED]  {OUT_XLSX}")
print(f"         {len(results)} query results written (one sheet each)")
print("="*60)
