# Power BI Dashboard – Setup Guide & DAX Measures
# HR Attrition Analytics Dashboard
# ============================================================

## STEP 1 – Import Data
# ---------------------------------------------------------
# 1. Open Power BI Desktop
# 2. Home → Get Data → Text/CSV
# 3. Load: data/hr_attrition_scored.csv   (primary table)
# 4. Rename table to: HR_Attrition

## STEP 2 – Data Model (Power Query transforms)
# ---------------------------------------------------------
# In Power Query Editor, verify these column types:
#   AttritionFlag          → Whole Number
#   MonthlyIncome          → Whole Number
#   Age                    → Whole Number
#   AttritionProb          → Decimal Number
#   YearsAtCompany         → Whole Number
#   SatisfactionIndex      → Decimal Number
#   All category columns   → Text

## STEP 3 – DAX Measures (paste into Model view → New Measure)
# ---------------------------------------------------------

# ── Core KPI Measures ──────────────────────────────────────

Total Employees =
    COUNTROWS(HR_Attrition)

Total Leavers =
    CALCULATE(COUNTROWS(HR_Attrition), HR_Attrition[Attrition] = "Yes")

Attrition Rate =
    DIVIDE([Total Leavers], [Total Employees], 0)

Attrition Rate % =
    FORMAT([Attrition Rate], "0.0%")

Avg Monthly Income =
    AVERAGE(HR_Attrition[MonthlyIncome])

Avg Income Leavers =
    CALCULATE(AVERAGE(HR_Attrition[MonthlyIncome]), HR_Attrition[Attrition] = "Yes")

Avg Income Stayers =
    CALCULATE(AVERAGE(HR_Attrition[MonthlyIncome]), HR_Attrition[Attrition] = "No")

Avg Tenure =
    AVERAGE(HR_Attrition[YearsAtCompany])

Avg Tenure Leavers =
    CALCULATE(AVERAGE(HR_Attrition[YearsAtCompany]), HR_Attrition[Attrition] = "Yes")

Avg Satisfaction =
    AVERAGE(HR_Attrition[SatisfactionIndex])

High Risk Count =
    CALCULATE(COUNTROWS(HR_Attrition),
              HR_Attrition[RiskTier] = "High",
              HR_Attrition[Attrition] = "No")

OverTime Attrition Rate =
    CALCULATE([Attrition Rate], HR_Attrition[OverTime] = "Yes")

# ── Variance / Comparison Measures ────────────────────────

Income Gap =
    [Avg Income Stayers] - [Avg Income Leavers]

Income Gap % =
    DIVIDE([Income Gap], [Avg Income Stayers], 0)

Dept Attrition vs Company Avg =
    [Attrition Rate] - CALCULATE([Attrition Rate], ALL(HR_Attrition[Department]))

# ── Conditional Formatting Measure ────────────────────────
# (Use this for KPI card background colours)

Attrition Alert Color =
    SWITCH(
        TRUE(),
        [Attrition Rate] >= 0.35, "Red",
        [Attrition Rate] >= 0.20, "Orange",
        "Green"
    )


## STEP 4 – Dashboard Pages & Visuals
# ---------------------------------------------------------

### PAGE 1 – Executive Overview
# ┌─────────────────────────────────────────────────────────┐
# │  KPI CARDS (top row)                                     │
# │  [Total Employees] [Total Leavers] [Attrition Rate %]   │
# │  [Avg Income] [Avg Tenure] [High Risk Count]            │
# ├─────────────────────────────────────────────────────────┤
# │  BAR CHART: Attrition Rate by Department                 │
# │    Axis: Department | Value: Attrition Rate              │
# │    Sort: Descending | Data labels: ON                   │
# ├──────────────────────┬──────────────────────────────────┤
# │  DONUT: Attrition    │  BAR: Attrition by Gender        │
# │  Yes vs No           │  Axis: Gender | Value: Rate      │
# └──────────────────────┴──────────────────────────────────┘

### PAGE 2 – Departmental Breakdown
# ┌─────────────────────────────────────────────────────────┐
# │  FILTER PANEL (top): Department slicer, Gender slicer   │
# ├─────────────────────────────────────────────────────────┤
# │  STACKED BAR: Attrition by Job Role                     │
# │    Y: JobRole | X: Count | Legend: Attrition            │
# ├─────────────────────────────────────────────────────────┤
# │  MATRIX TABLE: Department × JobRole attrition rates     │
# │    Rows: Department | Cols: JobRole | Values: Rate       │
# └─────────────────────────────────────────────────────────┘

### PAGE 3 – Demographics Analysis
# ┌─────────────────────────────────────────────────────────┐
# │  SLICERS: Gender | Education Level | Marital Status     │
# ├──────────────────────┬──────────────────────────────────┤
# │  BAR: Rate by        │  BAR: Rate by Education          │
# │  Age Group           │  Field                           │
# ├──────────────────────┴──────────────────────────────────┤
# │  CLUSTERED BAR: MaritalStatus × Attrition               │
# └─────────────────────────────────────────────────────────┘

### PAGE 4 – Salary & Satisfaction
# ┌─────────────────────────────────────────────────────────┐
# │  SCATTER: MonthlyIncome vs SatisfactionIndex            │
# │    X: SatisfactionIndex | Y: MonthlyIncome              │
# │    Size: YearsAtCompany | Legend: Attrition             │
# ├──────────────────────┬──────────────────────────────────┤
# │  BAR: Attrition Rate │  BAR: Rate by Business Travel    │
# │  by Income Band      │                                  │
# ├──────────────────────┴──────────────────────────────────┤
# │  KPI: Income Gap ($) between Leavers & Stayers          │
# └─────────────────────────────────────────────────────────┘

### PAGE 5 – Tenure & Risk
# ┌─────────────────────────────────────────────────────────┐
# │  LINE CHART: Headcount by Join Year (Q13 data)          │
# │    X: JoinYear | Y: TotalJoined, StillActive            │
# ├──────────────────────┬──────────────────────────────────┤
# │  BAR: Leavers by     │  TREEMAP: Risk Tier distribution │
# │  Tenure Bucket       │  Category: RiskTier | Size: Count│
# ├──────────────────────┴──────────────────────────────────┤
# │  TABLE: Top 10 High-Risk Employees (Active only)        │
# │  Cols: ID, Dept, Role, Income, Satisfaction, OverTime   │
# └─────────────────────────────────────────────────────────┘

## STEP 5 – Slicers / Filters (add to every page)
# ---------------------------------------------------------
# • Department          (dropdown)
# • Gender              (buttons)
# • Education_Label     (dropdown)
# • AgeGroup            (range slider or buttons)
# • OverTime            (toggle: Yes / No)
# • RiskTier            (buttons: Low / Medium / High)

## STEP 6 – Conditional Formatting Tips
# ---------------------------------------------------------
# • Attrition Rate KPI card: Red if >35%, Amber if >20%, Green otherwise
# • Table rows: Highlight RiskTier=High in light red background
# • Bar charts: Use diverging palette (red = high attrition)
#   Recommended: #E74C3C (red) / #F39C12 (amber) / #2ECC71 (green)

## STEP 7 – Publish & Share
# ---------------------------------------------------------
# 1. File → Publish → Publish to Power BI (requires Pro licence)
# 2. Or export as PDF: File → Export → Export to PDF
# 3. For GitHub: export screenshots to outputs/dashboard_screenshots/
