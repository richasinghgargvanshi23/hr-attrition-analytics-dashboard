"""
01_data_cleaning.py
────────────────────────────────────────────────────────────────────────────
HR Attrition Project  –  Week 1-2  |  Data Cleaning & Preprocessing
────────────────────────────────────────────────────────────────────────────
Input  : data/hr_attrition_raw.csv
Output : data/hr_attrition_clean.csv
"""

import os
import pandas as pd
import numpy as np

# ── Paths ────────────────────────────────────────────────────────────────────
BASE     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(BASE, "data", "hr_attrition_raw.csv")
OUT_PATH = os.path.join(BASE, "data", "hr_attrition_clean.csv")

print("=" * 60)
print("HR ATTRITION  –  DATA CLEANING")
print("=" * 60)

# ── 1. Load ───────────────────────────────────────────────────────────────────
df = pd.read_csv(RAW_PATH)
print(f"\n[LOAD]  {df.shape[0]} rows  ×  {df.shape[1]} columns")

# ── 2. Baseline quality report ────────────────────────────────────────────────
missing = df.isnull().sum()
missing = missing[missing > 0]
print(f"\n[MISSING VALUES]\n{missing.to_string()}")
print(f"\n[DUPLICATES]  {df.duplicated().sum()} duplicate rows")

# ── 3. Drop constant / non-informative columns ───────────────────────────────
drop_cols = [c for c in ["EmployeeCount", "Over18", "StandardHours"] if c in df.columns]
df.drop(columns=drop_cols, inplace=True)
print(f"\n[DROPPED]  constant columns: {drop_cols}")

# ── 4. Handle missing values ──────────────────────────────────────────────────
# Numeric  → median imputation
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    n = df[col].isnull().sum()
    if n:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f"   [IMPUTE numeric]  {col}: {n} nulls → median ({median_val:.0f})")

# Categorical → mode imputation
cat_cols = df.select_dtypes(include=["object", "str"]).columns
for col in cat_cols:
    n = df[col].isnull().sum()
    if n:
        mode_val = df[col].mode()[0]
        df[col] = df[col].fillna(mode_val)
        print(f"   [IMPUTE cat]     {col}: {n} nulls → mode ('{mode_val}')")

# ── 5. Remove duplicates ──────────────────────────────────────────────────────
before = len(df)
df.drop_duplicates(inplace=True)
print(f"\n[DEDUP]  removed {before - len(df)} duplicates")

# ── 6. Data-type corrections ──────────────────────────────────────────────────
df["Age"]           = df["Age"].fillna(df["Age"].median()).astype(int)
df["MonthlyIncome"] = df["MonthlyIncome"].fillna(df["MonthlyIncome"].median()).astype(int)

# Ordinal mappings (keep numeric AND labelled versions)
edu_map     = {1: "Below College", 2: "College", 3: "Bachelor",
               4: "Master",        5: "Doctor"}
rating_map  = {1: "Low", 2: "Good", 3: "Excellent", 4: "Outstanding"}
satisfy_map = {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}

df["Education_Label"]              = df["Education"].map(edu_map)
df["PerformanceRating_Label"]      = df["PerformanceRating"].map(rating_map)
df["JobSatisfaction_Label"]        = df["JobSatisfaction"].map(satisfy_map)
df["EnvironmentSatisfaction_Label"]= df["EnvironmentSatisfaction"].map(satisfy_map)
df["WorkLifeBalance_Label"]        = df["WorkLifeBalance"].map(satisfy_map)

# ── 7. Feature engineering  (Weeks 3-4 fields added here too) ────────────────

# Tenure buckets
bins   = [-1, 1, 3, 6, 10, 20, 100]
labels = ["<1 yr", "1-3 yrs", "3-6 yrs", "6-10 yrs", "10-20 yrs", "20+ yrs"]
df["TenureBucket"] = pd.cut(df["YearsAtCompany"], bins=bins, labels=labels)

# Age group
age_bins   = [17, 25, 35, 45, 55, 100]
age_labels = ["18-25", "26-35", "36-45", "46-55", "55+"]
df["AgeGroup"] = pd.cut(df["Age"], bins=age_bins, labels=age_labels)

# Income band
inc_bins   = [0, 3000, 6000, 10000, 15000, 999999]
inc_labels = ["<3K", "3K-6K", "6K-10K", "10K-15K", "15K+"]
df["IncomeBand"] = pd.cut(df["MonthlyIncome"], bins=inc_bins, labels=inc_labels)

# Attrition binary flag
df["AttritionFlag"] = (df["Attrition"] == "Yes").astype(int)

# Overall satisfaction index  (average of 4 satisfaction scores)
df["SatisfactionIndex"] = df[
    ["JobSatisfaction", "EnvironmentSatisfaction",
     "WorkLifeBalance", "RelationshipSatisfaction"]
].mean(axis=1).round(2)

# High-risk flag (simplified model)
df["HighRisk"] = (
    (df["AttritionFlag"] == 1) |
    (df["JobSatisfaction"] <= 2) |
    (df["SatisfactionIndex"] < 2.0) |
    (df["OverTime"] == "Yes")
).astype(int)

print("\n[FEATURES ADDED]")
new_cols = ["TenureBucket", "AgeGroup", "IncomeBand",
            "AttritionFlag", "SatisfactionIndex", "HighRisk",
            "Education_Label", "PerformanceRating_Label",
            "JobSatisfaction_Label", "EnvironmentSatisfaction_Label",
            "WorkLifeBalance_Label"]
for c in new_cols:
    print(f"   + {c}")

# ── 8. Validate ranges ────────────────────────────────────────────────────────
assert df["Age"].between(18, 100).all(),         "Age out of range"
assert df["MonthlyIncome"].gt(0).all(),           "Negative income"
assert df["Attrition"].isin(["Yes","No"]).all(),  "Unexpected Attrition value"
print("\n[VALIDATION]  All range checks passed ✓")

# ── 9. Save ───────────────────────────────────────────────────────────────────
df.to_csv(OUT_PATH, index=False)
print(f"\n[SAVED]  {OUT_PATH}")
print(f"         {df.shape[0]} rows  ×  {df.shape[1]} columns")
print(f"\n[ATTRITION RATE]  {df['AttritionFlag'].mean():.1%}")
print("\n" + "=" * 60)
print("Cleaning complete.")
print("=" * 60)
