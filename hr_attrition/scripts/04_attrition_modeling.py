"""
04_attrition_modeling.py
────────────────────────────────────────────────────────────────────────────
HR Attrition Project  –  Weeks 3-4  |  Predictive Modeling
────────────────────────────────────────────────────────────────────────────
Trains a Random Forest classifier to identify top attrition drivers.
Outputs: feature importance chart + scored dataset for dashboard.

Input  : data/hr_attrition_clean.csv
Output : outputs/eda_10_feature_importance.png
         data/hr_attrition_scored.csv
"""

import os
import warnings
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (classification_report, confusion_matrix,
                              roc_auc_score, ConfusionMatrixDisplay)

warnings.filterwarnings("ignore")

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA        = os.path.join(BASE, "data", "hr_attrition_clean.csv")
SCORED_PATH = os.path.join(BASE, "data", "hr_attrition_scored.csv")
OUT_DIR     = os.path.join(BASE, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams.update({"figure.dpi": 120, "savefig.bbox": "tight"})

print("=" * 60)
print("HR ATTRITION  –  PREDICTIVE MODELING")
print("=" * 60)

# ── Load & prepare features ───────────────────────────────────────────────────
df = pd.read_csv(DATA)

# Drop label-redundant or ID columns
drop_cols = [
    "AttritionFlag", "Attrition",
    "TenureBucket", "AgeGroup", "IncomeBand",          # derived from numerics
    "Education_Label", "PerformanceRating_Label",
    "JobSatisfaction_Label", "EnvironmentSatisfaction_Label",
    "WorkLifeBalance_Label", "HighRisk",
    "EmployeeID",
]
drop_cols = [c for c in drop_cols if c in df.columns]

X_raw = df.drop(columns=drop_cols)
y     = df["AttritionFlag"]

# Encode categoricals
cat_cols = X_raw.select_dtypes(include=["object", "category", "str"]).columns.tolist()
le_map   = {}
X        = X_raw.copy()
for col in cat_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    le_map[col] = le

print(f"\nFeatures : {X.shape[1]}  |  Samples : {len(y)}  |  "
      f"Attrition rate : {y.mean():.1%}")

# ── Train / test split ────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# ── Random Forest model ───────────────────────────────────────────────────────
rf = RandomForestClassifier(
    n_estimators=300, max_depth=10, min_samples_leaf=5,
    class_weight="balanced", random_state=42, n_jobs=-1
)
rf.fit(X_train, y_train)

y_pred     = rf.predict(X_test)
y_prob     = rf.predict_proba(X_test)[:, 1]
auc        = roc_auc_score(y_test, y_prob)
cv_scores  = cross_val_score(rf, X, y, cv=5, scoring="roc_auc")

print(f"\n[MODEL]  Random Forest")
print(f"  AUC (test)       : {auc:.4f}")
print(f"  AUC (5-fold CV)  : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
print("\n[CLASSIFICATION REPORT]")
print(classification_report(y_test, y_pred, target_names=["Stay", "Leave"]))

# ── Feature importance ────────────────────────────────────────────────────────
imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
top15 = imp.head(15)

fig, ax = plt.subplots(figsize=(10, 6))
colors = sns.color_palette("RdYlGn_r", len(top15))
ax.barh(top15.index[::-1], top15.values[::-1], color=colors[::-1])
ax.set_xlabel("Feature Importance (Gini)")
ax.set_title("Top 15 Attrition Drivers  –  Random Forest", fontweight="bold")
fig.savefig(os.path.join(OUT_DIR, "eda_10_feature_importance.png"))
plt.close()
print("\n[SAVED]  eda_10_feature_importance.png")

print("\n[TOP 15 ATTRITION DRIVERS]")
for feat, score in top15.items():
    bar = "█" * int(score * 200)
    print(f"  {feat:<35} {score:.4f}  {bar}")

# ── Confusion matrix ──────────────────────────────────────────────────────────
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                               display_labels=["Stay", "Leave"])
fig, ax = plt.subplots(figsize=(5, 4))
disp.plot(ax=ax, cmap="Blues", colorbar=False)
ax.set_title("Confusion Matrix  –  Random Forest", fontweight="bold")
fig.savefig(os.path.join(OUT_DIR, "eda_11_confusion_matrix.png"))
plt.close()
print("[SAVED]  eda_11_confusion_matrix.png")

# ── Score full dataset & save ─────────────────────────────────────────────────
df_scored        = df.copy()
df_scored["AttritionProb"] = rf.predict_proba(X)[:, 1].round(4)
df_scored["RiskTier"] = pd.cut(
    df_scored["AttritionProb"],
    bins=[0, 0.3, 0.6, 1.0],
    labels=["Low", "Medium", "High"]
)
df_scored.to_csv(SCORED_PATH, index=False)
print(f"\n[SAVED]  {SCORED_PATH}")

risk_dist = df_scored["RiskTier"].value_counts()
print(f"\n[RISK DISTRIBUTION]\n{risk_dist.to_string()}")

print("\n" + "=" * 60)
print("Modeling complete.")
print("=" * 60)
