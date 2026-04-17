"""
05_dashboard_preview.py
────────────────────────────────────────────────────────────────────────────
HR Attrition Project  –  Week 5  |  Static Dashboard Preview
────────────────────────────────────────────────────────────────────────────
Generates a multi-panel dashboard image suitable for GitHub README preview.
This replicates the Power BI layout as a static matplotlib figure.

Input  : data/hr_attrition_scored.csv
Output : outputs/dashboard_preview.png
"""

import os
import warnings
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter
import seaborn as sns

warnings.filterwarnings("ignore")

BASE    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA    = os.path.join(BASE, "data", "hr_attrition_scored.csv")
OUT_DIR = os.path.join(BASE, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(DATA)

# ── Colour constants ──────────────────────────────────────────────────────────
RED      = "#E74C3C"
GREEN    = "#2ECC71"
AMBER    = "#F39C12"
BLUE     = "#2980B9"
PURPLE   = "#8E44AD"
TEAL     = "#16A085"
BG       = "#F4F6F9"
CARD_BG  = "#FFFFFF"
TITLE_C  = "#2C3E50"

# ── Pre-compute metrics ───────────────────────────────────────────────────────
total_emp    = len(df)
total_leave  = (df["Attrition"] == "Yes").sum()
attr_rate    = total_leave / total_emp
avg_income   = df["MonthlyIncome"].mean()
avg_tenure   = df["YearsAtCompany"].mean()
high_risk    = ((df["RiskTier"] == "High") & (df["Attrition"] == "No")).sum()

dept_rate = (df.groupby("Department")["AttritionFlag"].mean() * 100).sort_values()
role_rate = (df.groupby("JobRole")["AttritionFlag"].mean() * 100).sort_values(ascending=False).head(7)
age_rate  = df.groupby("AgeGroup", observed=True)["AttritionFlag"].mean() * 100
inc_rate  = df.groupby("IncomeBand", observed=True)["AttritionFlag"].mean() * 100
risk_dist = df[df["Attrition"] == "No"]["RiskTier"].value_counts()
ot_vals   = df.groupby("OverTime")["AttritionFlag"].mean() * 100

# Headcount trend
df_head = df.copy()
df_head["JoinYear"] = 2024 - df_head["YearsAtCompany"]
hc = df_head.groupby("JoinYear").agg(
    TotalJoined=("EmployeeID", "count"),
    StillActive=("AttritionFlag", lambda x: (x == 0).sum())
).reset_index()
hc = hc[hc["JoinYear"].between(1985, 2024)]

# ── Canvas ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(22, 15), facecolor=BG)
fig.patch.set_facecolor(BG)

# Title banner
fig.text(0.5, 0.97, "HR ATTRITION ANALYTICS DASHBOARD",
         ha="center", va="top", fontsize=20, fontweight="bold",
         color=TITLE_C, fontfamily="DejaVu Sans")
fig.text(0.5, 0.945, "Interactive insight into employee turnover drivers | IBM-style HR Dataset",
         ha="center", va="top", fontsize=11, color="#7F8C8D")

# ── KPI row ───────────────────────────────────────────────────────────────────
kpi_specs = [
    (0.03, 0.86, "Total\nEmployees",  f"{total_emp:,}",    BLUE),
    (0.21, 0.86, "Total\nLeavers",    f"{total_leave:,}",  RED),
    (0.39, 0.86, "Attrition\nRate",   f"{attr_rate:.1%}",  RED if attr_rate > 0.25 else AMBER),
    (0.57, 0.86, "Avg Monthly\nIncome", f"${avg_income:,.0f}", GREEN),
    (0.75, 0.86, "Avg Tenure\n(yrs)", f"{avg_tenure:.1f}", TEAL),
    (0.87, 0.86, "High-Risk\nActive", f"{high_risk}",      AMBER),
]
for x, y, label, val, color in kpi_specs:
    ax_kpi = fig.add_axes([x, y, 0.11, 0.07], facecolor=CARD_BG)
    ax_kpi.set_xlim(0, 1); ax_kpi.set_ylim(0, 1)
    ax_kpi.axis("off")
    for spine in ax_kpi.spines.values():
        spine.set_visible(False)
    ax_kpi.text(0.5, 0.72, val, ha="center", va="center",
                fontsize=18, fontweight="bold", color=color)
    ax_kpi.text(0.5, 0.22, label, ha="center", va="center",
                fontsize=9, color="#7F8C8D", linespacing=1.3)
    rect = mpatches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02",
                                    linewidth=2, edgecolor=color, facecolor=CARD_BG)
    ax_kpi.add_patch(rect)

# ── Grid layout ───────────────────────────────────────────────────────────────
gs = gridspec.GridSpec(2, 4, figure=fig,
                       top=0.84, bottom=0.06,
                       left=0.04, right=0.98,
                       hspace=0.40, wspace=0.35)

# ─── Panel 1: Attrition by Department ────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(CARD_BG)
colors1 = [RED if v > 35 else AMBER if v > 25 else GREEN for v in dept_rate.values]
bars = ax1.barh(dept_rate.index, dept_rate.values, color=colors1,
                edgecolor="white", height=0.5)
for b in bars:
    ax1.text(b.get_width() + 0.5, b.get_y() + b.get_height()/2,
             f"{b.get_width():.1f}%", va="center", fontsize=9, color=TITLE_C)
ax1.set_title("Attrition Rate by Department", fontweight="bold", color=TITLE_C, pad=6)
ax1.set_xlabel("Attrition Rate (%)", fontsize=9)
ax1.set_xlim(0, dept_rate.max() * 1.25)
ax1.tick_params(labelsize=9)
ax1.spines[["top","right"]].set_visible(False)

# ─── Panel 2: Attrition by Job Role ──────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(CARD_BG)
role_colors = plt.cm.RdYlGn_r(np.linspace(0.1, 0.9, len(role_rate)))
bars2 = ax2.bar(range(len(role_rate)), role_rate.values,
                color=role_colors, edgecolor="white")
ax2.set_xticks(range(len(role_rate)))
ax2.set_xticklabels([r.replace(" ", "\n") for r in role_rate.index],
                    fontsize=7, rotation=0, ha="center")
ax2.set_ylabel("Attrition Rate (%)", fontsize=9)
ax2.set_title("Attrition by Job Role (Top 7)", fontweight="bold", color=TITLE_C, pad=6)
for b in bars2:
    ax2.text(b.get_x() + b.get_width()/2, b.get_height() + 0.4,
             f"{b.get_height():.0f}%", ha="center", fontsize=7.5)
ax2.spines[["top","right"]].set_visible(False)

# ─── Panel 3: Attrition by Age Group ─────────────────────────────────────────
ax3 = fig.add_subplot(gs[0, 2])
ax3.set_facecolor(CARD_BG)
age_colors = [RED if v > 40 else AMBER if v > 30 else GREEN for v in age_rate.values]
ax3.bar(age_rate.index.astype(str), age_rate.values,
        color=age_colors, edgecolor="white")
ax3.set_ylabel("Attrition Rate (%)", fontsize=9)
ax3.set_title("Attrition by Age Group", fontweight="bold", color=TITLE_C, pad=6)
ax3.tick_params(labelsize=9)
ax3.spines[["top","right"]].set_visible(False)

# ─── Panel 4: Risk Tier Donut ─────────────────────────────────────────────────
ax4 = fig.add_subplot(gs[0, 3])
ax4.set_facecolor(CARD_BG)
risk_order = ["High", "Medium", "Low"]
risk_vals  = [risk_dist.get(r, 0) for r in risk_order]
risk_colors= [RED, AMBER, GREEN]
wedges, texts, autotexts = ax4.pie(
    risk_vals, labels=risk_order, colors=risk_colors,
    autopct="%1.0f%%", startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 2},
    pctdistance=0.75
)
centre_circle = plt.Circle((0, 0), 0.5, fc=CARD_BG)
ax4.add_artist(centre_circle)
for t in autotexts: t.set_fontsize(9)
ax4.set_title("Active Employees – Risk Tier", fontweight="bold", color=TITLE_C, pad=6)

# ─── Panel 5: Headcount Trend (line chart) ────────────────────────────────────
ax5 = fig.add_subplot(gs[1, 0:2])
ax5.set_facecolor(CARD_BG)
ax5.plot(hc["JoinYear"], hc["TotalJoined"], color=BLUE,
         marker="o", ms=4, lw=2, label="Joined")
ax5.plot(hc["JoinYear"], hc["StillActive"], color=GREEN,
         marker="s", ms=4, lw=2, label="Still Active")
ax5.fill_between(hc["JoinYear"], hc["TotalJoined"], hc["StillActive"],
                 alpha=0.15, color=RED, label="Left Company")
ax5.set_xlabel("Join Year", fontsize=9)
ax5.set_ylabel("Employee Count", fontsize=9)
ax5.set_title("Headcount Trend by Join Year Cohort", fontweight="bold", color=TITLE_C, pad=6)
ax5.legend(fontsize=9, framealpha=0.5)
ax5.spines[["top","right"]].set_visible(False)
ax5.tick_params(labelsize=9)

# ─── Panel 6: Salary vs Attrition ─────────────────────────────────────────────
ax6 = fig.add_subplot(gs[1, 2])
ax6.set_facecolor(CARD_BG)
inc_order = ["<3K", "3K-6K", "6K-10K", "10K-15K", "15K+"]
inc_plot  = inc_rate.reindex(inc_order).dropna()
inc_c     = [RED if v > 40 else AMBER if v > 25 else GREEN for v in inc_plot.values]
ax6.bar(inc_plot.index.astype(str), inc_plot.values,
        color=inc_c, edgecolor="white")
ax6.set_ylabel("Attrition Rate (%)", fontsize=9)
ax6.set_title("Attrition by Income Band", fontweight="bold", color=TITLE_C, pad=6)
ax6.tick_params(labelsize=9)
ax6.spines[["top","right"]].set_visible(False)

# ─── Panel 7: OverTime Impact ─────────────────────────────────────────────────
ax7 = fig.add_subplot(gs[1, 3])
ax7.set_facecolor(CARD_BG)
ot_labels = ["No OverTime", "OverTime"]
ot_values = [ot_vals.get("No", 0), ot_vals.get("Yes", 0)]
ot_colors = [GREEN, RED]
bars7 = ax7.bar(ot_labels, ot_values, color=ot_colors, edgecolor="white", width=0.4)
for b in bars7:
    ax7.text(b.get_x() + b.get_width()/2, b.get_height() + 0.5,
             f"{b.get_height():.1f}%", ha="center", fontsize=11, fontweight="bold")
ax7.set_ylabel("Attrition Rate (%)", fontsize=9)
ax7.set_title("OverTime vs Attrition Rate", fontweight="bold", color=TITLE_C, pad=6)
ax7.set_ylim(0, max(ot_values) * 1.2)
ax7.spines[["top","right"]].set_visible(False)
ax7.tick_params(labelsize=10)

# ── Footer ────────────────────────────────────────────────────────────────────
fig.text(0.5, 0.02,
         "Source: IBM HR Analytics Dataset  |  Model: Random Forest  |  "
         "Filters available in Power BI: Department · Gender · Education · Age Group · Risk Tier",
         ha="center", fontsize=8, color="#95A5A6")

out_path = os.path.join(OUT_DIR, "dashboard_preview.png")
plt.savefig(out_path, dpi=130, facecolor=BG, bbox_inches="tight")
plt.close()
print(f"[SAVED]  {out_path}")
print("Dashboard preview generated successfully.")
