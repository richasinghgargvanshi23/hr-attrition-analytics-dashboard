-- ============================================================
-- HR Attrition Analytics  –  SQL Query Library
-- ============================================================
-- Engine : SQLite (via hr_sql_queries.py runner)
--          Compatible with PostgreSQL / MySQL with minor tweaks
-- Table  : hr_attrition
-- ============================================================

-- ──────────────────────────────────────────────────────────
-- Q1. Overall attrition count & rate
-- ──────────────────────────────────────────────────────────
SELECT
    Attrition,
    COUNT(*)                                          AS Employees,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS PctOfTotal
FROM hr_attrition
GROUP BY Attrition
ORDER BY Employees DESC;


-- ──────────────────────────────────────────────────────────
-- Q2. Attrition by Department
-- ──────────────────────────────────────────────────────────
SELECT
    Department,
    COUNT(*)                                           AS Total,
    SUM(AttritionFlag)                                 AS Leavers,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2)   AS AttritionRate_pct
FROM hr_attrition
GROUP BY Department
ORDER BY AttritionRate_pct DESC;


-- ──────────────────────────────────────────────────────────
-- Q3. Attrition by Job Role
-- ──────────────────────────────────────────────────────────
SELECT
    JobRole,
    Department,
    COUNT(*)                                           AS Total,
    SUM(AttritionFlag)                                 AS Leavers,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2)   AS AttritionRate_pct
FROM hr_attrition
GROUP BY JobRole, Department
ORDER BY AttritionRate_pct DESC;


-- ──────────────────────────────────────────────────────────
-- Q4. Attrition by Age Group
-- ──────────────────────────────────────────────────────────
SELECT
    AgeGroup,
    COUNT(*)                                           AS Total,
    SUM(AttritionFlag)                                 AS Leavers,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2)   AS AttritionRate_pct
FROM hr_attrition
GROUP BY AgeGroup
ORDER BY AgeGroup;


-- ──────────────────────────────────────────────────────────
-- Q5. All attriting employees (raw filter)
-- ──────────────────────────────────────────────────────────
SELECT
    EmployeeID, Age, Department, JobRole,
    MonthlyIncome, YearsAtCompany,
    JobSatisfaction, OverTime, MaritalStatus
FROM hr_attrition
WHERE Attrition = 'Yes'
ORDER BY YearsAtCompany;


-- ──────────────────────────────────────────────────────────
-- Q6. Average tenure & income by attrition status
-- ──────────────────────────────────────────────────────────
SELECT
    Attrition,
    ROUND(AVG(YearsAtCompany), 2)  AS AvgTenure_yrs,
    ROUND(AVG(MonthlyIncome), 0)   AS AvgMonthlyIncome,
    ROUND(AVG(JobSatisfaction), 2) AS AvgJobSatisfaction,
    ROUND(AVG(SatisfactionIndex), 2) AS AvgSatisfactionIndex
FROM hr_attrition
GROUP BY Attrition;


-- ──────────────────────────────────────────────────────────
-- Q7. Impact of Overtime on attrition
-- ──────────────────────────────────────────────────────────
SELECT
    OverTime,
    COUNT(*)                                           AS Total,
    SUM(AttritionFlag)                                 AS Leavers,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2)   AS AttritionRate_pct
FROM hr_attrition
GROUP BY OverTime;


-- ──────────────────────────────────────────────────────────
-- Q8. Attrition by Tenure Bucket
-- ──────────────────────────────────────────────────────────
SELECT
    TenureBucket,
    COUNT(*)                                           AS Total,
    SUM(AttritionFlag)                                 AS Leavers,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2)   AS AttritionRate_pct
FROM hr_attrition
GROUP BY TenureBucket
ORDER BY
    CASE TenureBucket
        WHEN '<1 yr'    THEN 1
        WHEN '1-3 yrs'  THEN 2
        WHEN '3-6 yrs'  THEN 3
        WHEN '6-10 yrs' THEN 4
        WHEN '10-20 yrs'THEN 5
        ELSE 6
    END;


-- ──────────────────────────────────────────────────────────
-- Q9. Salary vs. Attrition (income band breakdown)
-- ──────────────────────────────────────────────────────────
SELECT
    IncomeBand,
    COUNT(*)                                           AS Total,
    SUM(AttritionFlag)                                 AS Leavers,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2)   AS AttritionRate_pct
FROM hr_attrition
GROUP BY IncomeBand
ORDER BY
    CASE IncomeBand
        WHEN '<3K'     THEN 1
        WHEN '3K-6K'   THEN 2
        WHEN '6K-10K'  THEN 3
        WHEN '10K-15K' THEN 4
        ELSE 5
    END;


-- ──────────────────────────────────────────────────────────
-- Q10. Gender-based attrition
-- ──────────────────────────────────────────────────────────
SELECT
    Gender,
    COUNT(*)                                           AS Total,
    SUM(AttritionFlag)                                 AS Leavers,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2)   AS AttritionRate_pct
FROM hr_attrition
GROUP BY Gender;


-- ──────────────────────────────────────────────────────────
-- Q11. Education Level vs Attrition
-- ──────────────────────────────────────────────────────────
SELECT
    Education_Label,
    Education,
    COUNT(*)                                           AS Total,
    SUM(AttritionFlag)                                 AS Leavers,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2)   AS AttritionRate_pct
FROM hr_attrition
GROUP BY Education_Label, Education
ORDER BY Education;


-- ──────────────────────────────────────────────────────────
-- Q12. Top 10 high-risk employees (for HR action)
-- ──────────────────────────────────────────────────────────
SELECT
    EmployeeID, Age, Department, JobRole,
    MonthlyIncome, YearsAtCompany,
    JobSatisfaction, EnvironmentSatisfaction,
    WorkLifeBalance, OverTime,
    SatisfactionIndex
FROM hr_attrition
WHERE Attrition = 'No'           -- still employed
  AND JobSatisfaction <= 2
  AND OverTime = 'Yes'
ORDER BY SatisfactionIndex ASC
LIMIT 10;


-- ──────────────────────────────────────────────────────────
-- Q13. Headcount trend simulation by tenure cohort
--      (mimics a time-series view for Power BI)
-- ──────────────────────────────────────────────────────────
SELECT
    (strftime('%Y', 'now') - YearsAtCompany)   AS JoinYear,
    COUNT(*)                                    AS TotalJoined,
    SUM(AttritionFlag)                          AS TotalLeft,
    COUNT(*) - SUM(AttritionFlag)               AS StillActive
FROM hr_attrition
GROUP BY JoinYear
ORDER BY JoinYear;


-- ──────────────────────────────────────────────────────────
-- Q14. Marital status & attrition
-- ──────────────────────────────────────────────────────────
SELECT
    MaritalStatus,
    COUNT(*)                                           AS Total,
    SUM(AttritionFlag)                                 AS Leavers,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2)   AS AttritionRate_pct
FROM hr_attrition
GROUP BY MaritalStatus
ORDER BY AttritionRate_pct DESC;


-- ──────────────────────────────────────────────────────────
-- Q15. Business Travel vs Attrition
-- ──────────────────────────────────────────────────────────
SELECT
    BusinessTravel,
    COUNT(*)                                           AS Total,
    SUM(AttritionFlag)                                 AS Leavers,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2)   AS AttritionRate_pct
FROM hr_attrition
GROUP BY BusinessTravel
ORDER BY AttritionRate_pct DESC;
