-- Description: Define period mappings for MBIE Jobs Online to support analysis
-- Reference: 
  -- Jobs Online: https://www.mbie.govt.nz/business-and-employment/employment-and-skills/labour-market-reports-data-and-analysis/jobs-online
  -- Seasonality analysis: https://zeilsoftware.atlassian.net/wiki/spaces/ZEIL/pages/539262981/UoA+Datascience+Internships+-+Seasonal+Modelling+Visualisation#Overall-Job-Vacancies-Index

WITH mapping AS (
  SELECT 
    DATE('2010-01-01') AS date_begin, 
    DATE('2019-12-31') AS date_end,
    'Uptrend (2010-2019)' AS period UNION ALL
  SELECT
    DATE('2023-01-01') AS date_begin,
    DATE('2050-12-31') AS date_end,
    'Downtrend (2023-NOW)' AS period
)
SELECT * FROM mapping;
