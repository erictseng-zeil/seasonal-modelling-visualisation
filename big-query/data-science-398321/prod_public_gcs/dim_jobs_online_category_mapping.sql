-- Description: Define category mappings for MBIE Jobs Online to support analysis
-- Reference: 
  -- Jobs Online: https://www.mbie.govt.nz/business-and-employment/employment-and-skills/labour-market-reports-data-and-analysis/jobs-online

WITH mapping AS (
  SELECT 'Total' AS category, 'TOTALS' AS subcategory UNION ALL
  # Skill Type
  SELECT 'Skill_Type', 'SkilledIndex' UNION ALL
  SELECT 'Skill_Type', 'UnskilledIndex' UNION ALL
  # Region
  SELECT 'Region', 'Auckland' UNION ALL
  SELECT 'Region', 'Wellington' UNION ALL
  SELECT 'Region', 'North_Island_Other' UNION ALL
  SELECT 'Region', 'Canterbury' UNION ALL
  SELECT 'Region', 'South_Island_Other' UNION ALL
  # Industry
  SELECT 'Industry', 'Business_services' UNION ALL
  SELECT 'Industry', 'Construction' UNION ALL
  SELECT 'Industry', 'Education' UNION ALL
  SELECT 'Industry', 'Health_care' UNION ALL
  SELECT 'Industry', 'Hospitality' UNION ALL
  SELECT 'Industry', 'IT' UNION ALL
  SELECT 'Industry', 'Manufacturing' UNION ALL
  SELECT 'Industry', 'Primary' UNION ALL
  SELECT 'Industry', 'Sales' UNION ALL
  SELECT 'Industry', 'Other' UNION ALL
  # Occupation
  SELECT 'Occupation', 'Managers' UNION ALL
  SELECT 'Occupation', 'Professionals' UNION ALL
  SELECT 'Occupation', 'Technicians_and_Trades_Workers' UNION ALL
  SELECT 'Occupation', 'Community_and_Personal_Service_Workers' UNION ALL
  SELECT 'Occupation', 'Clerical_and_Administrative_Workers' UNION ALL
  SELECT 'Occupation', 'Sales_Workers' UNION ALL
  SELECT 'Occupation', 'Machinery_Operators_and_Drivers' UNION ALL
  SELECT 'Occupation', 'Labourers' UNION ALL
  # Skill Level
  SELECT 'Skill_Level', 'Highly_Skilled' UNION ALL
  SELECT 'Skill_Level', 'Skilled' UNION ALL
  SELECT 'Skill_Level', 'Semi_Skilled' UNION ALL
  SELECT 'Skill_Level', 'Low_Skilled' UNION ALL
  SELECT 'Skill_Level', 'Unskilled'
)
SELECT * FROM mapping;
