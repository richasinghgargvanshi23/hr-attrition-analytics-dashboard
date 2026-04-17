"""
02_exploratory_analysis.py
────────────────────────────────────────────────────────────────────────────
HR Attrition Project  –  Week 1-2  |  Exploratory Data Analysis
────────────────────────────────────────────────────────────────────────────
Input  : data/hr_attrition_clean.csv
Output : outputs/eda_*.png  +  console summary
"""

import os
import warnings
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

warnings.filterwarnings("ignore")

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA     = os.path.join(BASE, "data", "hr_attrition_clean.csv")
OUT_DIR  = os.path.join(BASE, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Style ─────────────────────────────────────────────────────────────────────
PALETTE  = {"Yes": "#E74C3C", "No": "#2ECC71"}
sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams.update({"figure.dpi": 120, "savefig.bbox": "tight"})

df = pd.read_csv(DATA)
print("=" * 60)
print("EDA  –  HR ATTRITION DATASET")
print("=" * 60)
print(f"Shape: {df.shape}")
print(f"Attrition  Yes: {(df['Attrition']=='Yes').sum()}  "
      f"({df['AttritionFlag'].mean():.1%})")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Overall attrition pie
# ─────────────────────────────────────────────────────────────────────────────
counts = df["Attrition"].value_counts()
fig, ax = plt.subplots(figsize=(5, 5))
ax.pie(counts, labels=counts.index, autopct="%1.1f%%",
       colors=[PALETTE[k] for k in counts.index],
       startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 2})
ax.set_title("Overall Attrition Rate", fontsize=14, fontweight="bold")
fig.savefig(os.path.join(OUT_DIR, "eda_01_overall_attrition.png"))
plt.close()
print("\n[SAVED]  eda_01_overall_attrition.png")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Attrition by Department
# ─────────────────────────────────────────────────────────────────────────────
dept_attr = (df.groupby("Department")["AttritionFlag"]
               .agg(["mean", "count"])
               .rename(columns={"mean": "Rate", "count": "Total"})
               .sort_values("Rate", ascending=False))
dept_attr["Rate_pct"] = dept_attr["Rate"] * 100

fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.barh(dept_attr.index, dept_attr["Rate_pct"],
               color=["#E74C3C", "#E67E22", "#F39C12"])
ax.bar_label(bars, fmt="%.1f%%", padding=4)
ax.set_xlabel("Attrition Rate (%)")
ax.set_title("Attrition Rate by Department", fontweight="bold")
ax.set_xlim(0, dept_attr["Rate_pct"].max() * 1.25)
fig.savefig(os.path.join(OUT_DIR, "eda_02_attrition_by_dept.png"))
plt.close()
print("[SAVED]  eda_02_attrition_by_dept.png")

print("\n[DEPT ATTRITION RATES]")
print(dept_attr[["Rate_pct", "Total"]].to_string())

# ─────────────────────────────────────────────────────────────────────────────
# 3. Attrition by Job Role
# ─────────────────────────────────────────────────────────────────────────────
role_attr = (df.groupby("JobRole")["AttritionFlag"]
               .mean()
               .sort_values(ascending=False) * 100)

fig, ax = plt.subplots(figsize=(10, 5))
role_attr.plot(kind="bar", ax=ax, color="#3498DB", edgecolor="white")
ax.set_ylabel("Attrition Rate (%)")
ax.set_title("Attrition Rate by Job Role", fontweight="bold")
ax.set_xticklabels(ax.get_xticklabels(), rotation=35, ha="right")
for p in ax.patches:
    ax.annotate(f"{p.get_height():.1f}%",
                (p.get_x() + p.get_width() / 2, p.get_height() + 0.5),
                ha="center", va="bottom", fontsize=9)
fig.savefig(os.path.join(OUT_DIR, "eda_03_attrition_by_role.png"))
plt.close()
print("[SAVED]  eda_03_attrition_by_role.png")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Attrition by Age Group
# ─────────────────────────────────────────────────────────────────────────────
age_attr = (df.groupby("AgeGroup", observed=True)["AttritionFlag"]
              .mean() * 100)

fig, ax = plt.subplots(figsize=(7, 4))
age_attr.plot(kind="bar", ax=ax, color="#9B59B6", edgecolor="white")
ax.set_ylabel("Attrition Rate (%)")
ax.set_xlabel("Age Group")
ax.set_title("Attrition Rate by Age Group", fontweight="bold")
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
for p in ax.patches:
    ax.annotate(f"{p.get_height():.1f}%",
                (p.get_x() + p.get_width() / 2, p.get_height() + 0.3),
                ha="center", va="bottom", fontsize=10)
fig.savefig(os.path.join(OUT_DIR, "eda_04_attrition_by_age.png"))
plt.close()
print("[SAVED]  eda_04_attrition_by_age.png")

# ─────────────────────────────────────────────────────────────────────────────
# 5. Income distribution  (Leavers vs Stayers)
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4))
for label, grp in df.groupby("Attrition"):
    sns.kdeplot(grp["MonthlyIncome"], ax=ax, fill=True,
                label=f"Attrition={label}", alpha=0.4, color=PALETTE[label])
ax.set_xlabel("Monthly Income ($)")
ax.set_title("Income Distribution: Leavers vs Stayers", fontweight="bold")
ax.legend()
fig.savefig(os.path.join(OUT_DIR, "eda_05_income_distribution.png"))
plt.close()
print("[SAVED]  eda_05_income_distribution.png")

# ─────────────────────────────────────────────────────────────────────────────
# 6. Overtime vs Attrition
# ─────────────────────────────────────────────────────────────────────────────
ot_attr = df.groupby(["OverTime", "Attrition"]).size().unstack(fill_value=0)
ot_pct  = ot_attr.div(ot_attr.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(6, 4))
ot_pct.plot(kind="bar", ax=ax, color=[PALETTE["No"], PALETTE["Yes"]],
            edgecolor="white")
ax.set_ylabel("Percentage (%)")
ax.set_xlabel("OverTime")
ax.set_title("Attrition Rate: OverTime vs No OverTime", fontweight="bold")
ax.set_xticklabels(["No OverTime", "OverTime"], rotation=0)
ax.legend(title="Attrition", labels=["No", "Yes"])
fig.savefig(os.path.join(OUT_DIR, "eda_06_overtime_attrition.png"))
plt.close()
print("[SAVED]  eda_06_overtime_attrition.png")

# ─────────────────────────────────────────────────────────────────────────────
# 7. Correlation heatmap (numeric features)
# ─────────────────────────────────────────────────────────────────────────────
num_features = [
    "Age", "MonthlyIncome", "TotalWorkingYears", "YearsAtCompany",
    "JobSatisfaction", "EnvironmentSatisfaction", "WorkLifeBalance",
    "DistanceFromHome", "NumCompaniesWorked", "SatisfactionIndex",
    "AttritionFlag"
]
corr = df[num_features].corr()

fig, ax = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdYlGn",
            center=0, ax=ax, linewidths=0.5, cbar_kws={"shrink": 0.8})
ax.set_title("Correlation Matrix – Key Numeric Features", fontweight="bold")
fig.savefig(os.path.join(OUT_DIR, "eda_07_correlation_heatmap.png"))
plt.close()
print("[SAVED]  eda_07_correlation_heatmap.png")

# ─────────────────────────────────────────────────────────────────────────────
# 8. Satisfaction Index vs Attrition (scatter)
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 4))
for label, grp in df.groupby("Attrition"):
    ax.scatter(grp["SatisfactionIndex"], grp["MonthlyIncome"],
               alpha=0.25, s=20, label=f"Attrition={label}",
               color=PALETTE[label])
ax.set_xlabel("Satisfaction Index (1–4)")
ax.set_ylabel("Monthly Income ($)")
ax.set_title("Satisfaction vs Income (coloured by Attrition)", fontweight="bold")
ax.legend()
fig.savefig(os.path.join(OUT_DIR, "eda_08_satisfaction_scatter.png"))
plt.close()
print("[SAVED]  eda_08_satisfaction_scatter.png")

# ─────────────────────────────────────────────────────────────────────────────
# 9. Tenure distribution of leavers
# ─────────────────────────────────────────────────────────────────────────────
leavers = df[df["Attrition"] == "Yes"]
tenure_counts = (leavers["TenureBucket"]
                 .value_counts()
                 .reindex(["<1 yr","1-3 yrs","3-6 yrs",
                            "6-10 yrs","10-20 yrs","20+ yrs"]))

fig, ax = plt.subplots(figsize=(8, 4))
tenure_counts.plot(kind="bar", ax=ax, color="#1ABC9C", edgecolor="white")
ax.set_ylabel("Number of Leavers")
ax.set_xlabel("Tenure at Company")
ax.set_title("Leavers by Tenure Bucket", fontweight="bold")
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
fig.savefig(os.path.join(OUT_DIR, "eda_09_tenure_leavers.png"))
plt.close()
print("[SAVED]  eda_09_tenure_leavers.png")

# ─────────────────────────────────────────────────────────────────────────────
# Summary statistics
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SUMMARY STATISTICS")
print("=" * 60)

leavers_avg_tenure  = df[df["Attrition"]=="Yes"]["YearsAtCompany"].mean()
stayers_avg_tenure  = df[df["Attrition"]=="No"]["YearsAtCompany"].mean()
leavers_avg_income  = df[df["Attrition"]=="Yes"]["MonthlyIncome"].mean()
stayers_avg_income  = df[df["Attrition"]=="No"]["MonthlyIncome"].mean()
ot_attrition_rate   = df[df["OverTime"]=="Yes"]["AttritionFlag"].mean()
no_ot_attrition_rate= df[df["OverTime"]=="No"]["AttritionFlag"].mean()

print(f"Average tenure  – Leavers : {leavers_avg_tenure:.1f} yrs  | "
      f"Stayers : {stayers_avg_tenure:.1f} yrs")
print(f"Average income  – Leavers : ${leavers_avg_income:,.0f}  | "
      f"Stayers : ${stayers_avg_income:,.0f}")
print(f"Attrition rate  – OverTime Yes : {ot_attrition_rate:.1%}  | "
      f"No : {no_ot_attrition_rate:.1%}")
print(f"\nTop 3 departments by attrition:")
print(dept_attr[["Rate_pct"]].head(3).to_string())
print(f"\nTop 3 roles by attrition:")
print(role_attr.head(3).to_string())
print("\n" + "=" * 60)
print("EDA complete.  All charts saved to outputs/")
print("=" * 60)
