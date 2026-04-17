"""
Generate a realistic IBM-style HR Attrition dataset.
Run this script to create data/hr_attrition_raw.csv
"""

import pandas as pd
import numpy as np

np.random.seed(42)
N = 1470  # IBM dataset standard size

departments     = ["Sales", "Research & Development", "Human Resources"]
dept_weights    = [0.30, 0.60, 0.10]

job_roles = {
    "Sales":                   ["Sales Executive", "Sales Representative", "Manager"],
    "Research & Development":  ["Research Scientist", "Laboratory Technician",
                                 "Manufacturing Director", "Healthcare Representative",
                                 "Research Director", "Manager"],
    "Human Resources":         ["Human Resources", "Manager"],
}

education_fields = ["Life Sciences", "Medical", "Marketing",
                    "Technical Degree", "Human Resources", "Other"]
marital_statuses = ["Single", "Married", "Divorced"]
genders          = ["Male", "Female"]
business_travel  = ["Non-Travel", "Travel_Rarely", "Travel_Frequently"]
over_time        = ["Yes", "No"]

def sample_role(dept):
    return np.random.choice(job_roles[dept])

dept_col       = np.random.choice(departments, size=N, p=dept_weights)
job_role_col   = np.array([sample_role(d) for d in dept_col])
age_col        = np.random.randint(18, 61, size=N)
gender_col     = np.random.choice(genders, size=N, p=[0.60, 0.40])
marital_col    = np.random.choice(marital_statuses, size=N, p=[0.32, 0.46, 0.22])
edu_col        = np.random.randint(1, 6, size=N)          # 1-5
edu_field_col  = np.random.choice(education_fields, size=N)
travel_col     = np.random.choice(business_travel, size=N, p=[0.19, 0.71, 0.10])
ot_col         = np.random.choice(over_time, size=N, p=[0.28, 0.72])

years_col          = np.random.randint(0, 41, size=N)
years_current_col  = np.clip(np.random.randint(0, years_col + 1), 0, years_col)
years_mgr_col      = np.clip(np.random.randint(0, years_current_col + 1), 0, years_current_col)

monthly_income_col = np.random.randint(1000, 20000, size=N)
# Adjust income by education
monthly_income_col = (monthly_income_col * (0.7 + edu_col * 0.1)).astype(int)
monthly_income_col = np.clip(monthly_income_col, 1009, 19999)

job_level_col         = np.random.randint(1, 6, size=N)
job_satisfaction_col  = np.random.randint(1, 5, size=N)
env_satisfaction_col  = np.random.randint(1, 5, size=N)
work_life_col         = np.random.randint(1, 5, size=N)
relationship_col      = np.random.randint(1, 5, size=N)
perf_rating_col       = np.random.choice([3, 4], size=N, p=[0.85, 0.15])
job_involvement_col   = np.random.randint(1, 5, size=N)
num_companies_col     = np.random.randint(0, 10, size=N)
training_col          = np.random.randint(0, 7, size=N)
pct_hike_col          = np.random.randint(11, 26, size=N)
distance_col          = np.random.randint(1, 30, size=N)
stock_option_col      = np.random.randint(0, 4, size=N)

# ----- Attrition logic (realistic probability) -----
attrition_prob = np.full(N, 0.12)
attrition_prob[ot_col == "Yes"]                            += 0.15
attrition_prob[job_satisfaction_col <= 2]                  += 0.10
attrition_prob[work_life_col <= 2]                         += 0.08
attrition_prob[marital_col == "Single"]                    += 0.06
attrition_prob[travel_col == "Travel_Frequently"]          += 0.07
attrition_prob[years_col <= 2]                             += 0.12
attrition_prob[monthly_income_col < 3000]                  += 0.09
attrition_prob[distance_col > 20]                          += 0.05
attrition_prob[dept_col == "Sales"]                        += 0.05
attrition_prob[job_involvement_col <= 2]                   += 0.07
attrition_prob[env_satisfaction_col <= 2]                  += 0.05
attrition_prob = np.clip(attrition_prob, 0, 0.90)

attrition_col = np.where(np.random.rand(N) < attrition_prob, "Yes", "No")

df = pd.DataFrame({
    "EmployeeID":              range(1, N + 1),
    "Age":                     age_col,
    "Attrition":               attrition_col,
    "BusinessTravel":          travel_col,
    "DailyRate":               np.random.randint(100, 1500, N),
    "Department":              dept_col,
    "DistanceFromHome":        distance_col,
    "Education":               edu_col,
    "EducationField":          edu_field_col,
    "EmployeeCount":           1,
    "EnvironmentSatisfaction": env_satisfaction_col,
    "Gender":                  gender_col,
    "HourlyRate":              np.random.randint(30, 100, N),
    "JobInvolvement":          job_involvement_col,
    "JobLevel":                job_level_col,
    "JobRole":                 job_role_col,
    "JobSatisfaction":         job_satisfaction_col,
    "MaritalStatus":           marital_col,
    "MonthlyIncome":           monthly_income_col,
    "MonthlyRate":             np.random.randint(2000, 27000, N),
    "NumCompaniesWorked":      num_companies_col,
    "Over18":                  "Y",
    "OverTime":                ot_col,
    "PercentSalaryHike":       pct_hike_col,
    "PerformanceRating":       perf_rating_col,
    "RelationshipSatisfaction":relationship_col,
    "StandardHours":           80,
    "StockOptionLevel":        stock_option_col,
    "TotalWorkingYears":       years_col,
    "TrainingTimesLastYear":   training_col,
    "WorkLifeBalance":         work_life_col,
    "YearsAtCompany":          years_col,
    "YearsInCurrentRole":      years_current_col,
    "YearsSinceLastPromotion": np.random.randint(0, 16, N),
    "YearsWithCurrManager":    years_mgr_col,
})

# Intentionally inject a few issues for cleaning demo
df.loc[np.random.choice(df.index, 15, replace=False), "MonthlyIncome"] = np.nan
df.loc[np.random.choice(df.index, 10, replace=False), "Age"] = np.nan
df.loc[np.random.choice(df.index,  5, replace=False), "Department"] = None

df.to_csv("data/hr_attrition_raw.csv", index=False)
print(f"✅  Dataset saved → data/hr_attrition_raw.csv  ({len(df)} rows, {df.shape[1]} cols)")
print(f"   Attrition rate: {(df['Attrition']=='Yes').mean():.1%}")
