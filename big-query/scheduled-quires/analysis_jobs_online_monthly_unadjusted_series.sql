SELECT
  PARSE_DATE('%Y-%d-%m', CAST(jom.ACTUAL_DATE AS STRING)) AS date,
  jop.period,
  joc.category,
  jom.subcategory,
  CAST(jom.job_index AS FLOAT64) AS job_index
FROM `data-science-398321.prod_public_gcs.fact_jobs_online_monthly_unadjusted_series`
UNPIVOT (job_index FOR subcategory IN (
  TOTALS,
  SkilledIndex,
  UnskilledIndex,
  Auckland,
  Wellington,
  North_Island_Other,
  Canterbury,
  South_Island_Other,
  Business_services,
  Construction,
  Education,
  Health_care,
  Hospitality,
  IT,
  Manufacturing,
  Primary,
  Sales,
  Other,
  Managers,
  Professionals,
  Technicians_and_Trades_Workers,
  Community_and_Personal_Service_Workers,
  Clerical_and_Administrative_Workers,
  Sales_Workers,
  Machinery_Operators_and_Drivers,
  Labourers,
  Highly_Skilled,
  Skilled,
  Semi_Skilled,
  Low_Skilled,
  Unskilled
)) AS jom
LEFT JOIN `data-science-398321.prod_public_gcs.dim_jobs_online_category_mapping` AS joc
USING (subcategory)
LEFT JOIN `data-science-398321.prod_public_gcs.dim_jobs_online_period_mapping` AS jop 
  ON PARSE_DATE('%Y-%d-%m', CAST(jom.ACTUAL_DATE AS STRING)) BETWEEN jop.date_begin AND jop.date_end