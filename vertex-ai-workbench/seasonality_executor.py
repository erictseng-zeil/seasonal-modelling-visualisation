# %%
# -- Import data from BigQuery -- #
import pandas_gbq

project_id = 'data-science-398321'
query = """
SELECT
  date,
  period,
  category,
  subcategory,
  job_index
FROM `data-science-398321.prod_marketing.jobs_online_monthly_unadjusted_series`
WHERE period IS NOT NULL # Exclude periods of high fluctuation
"""

df = pandas_gbq.read_gbq(query, project_id=project_id)


# %%
print(f"rows: {len(df)}")
df.head(5)


# %%
# -- Seasonal decompose each column -- #
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import pandas as pd

def decompose_by_period_subcategory(
    df, period=12, model='additive',
    two_sided=True, extrapolate_trend=0):

    results = []

    # Group by period and category/subcategory
    for (p, cat, subcat), group in df.groupby(["period", "category", "subcategory"]):
        group = group.sort_values("date").set_index("date")

        result = seasonal_decompose(
            group["job_index"],
            model=model,
            period=period,
            two_sided=two_sided,
            extrapolate_trend=extrapolate_trend
        )

        # DataFrame
        tmp = pd.DataFrame({
            "date": group.index,
            "period": p,
            "category": cat,
            "subcategory": subcat,
            "observed": result.observed.values,
            "trend": result.trend.values,
            "seasonal": result.seasonal.values,
            "resid": result.resid.values
        })
        results.append(tmp)

    # Concat results
    results_df = pd.concat(results, ignore_index=True)
    results_df['date'] = pd.to_datetime(results_df['date']).dt.date
    return results_df


# %%
decompose_df = decompose_by_period_subcategory(df, extrapolate_trend=6)
decompose_df.head(5)

# %%
# -- Push data to BigQuery -- #
from pandas_gbq import to_gbq

project_id = "data-science-398321"
dataset = "prod_marketing"
table = "jobs_online_monthly_seasonality"

to_gbq(
    decompose_df,
    destination_table=f"{dataset}.{table}",
    project_id=project_id,
    if_exists="replace"  # or "append"
)


# %%
# Check the uploaded data
from google.cloud import bigquery

table_id = f"{project_id}.{dataset}.{table}"
sql = f"""
SELECT
  COUNT(*) AS n_rows,
FROM `{table_id}`
"""

check_df = pandas_gbq.read_gbq(query, project_id=project_id)


# %%
print(f"rows: {len(check_df)}")
check_df.head(5)


# %%
# -- Check residual summary -- #
# If it's high, we may not see the seasonal patterns are stable
import pandas as pd
import numpy as np

def residual_summary(decompose_df, period, category):
    # specific category
    
    df = decompose_df[decompose_df["period"] == period].copy()
    df = df[df['category'] == category]
    
    # rmse
    summary = (df.groupby("subcategory")
               .apply(lambda g: pd.Series({
                   "rmse": np.sqrt(np.mean(g["resid"].dropna()**2)),
                   "mae": g["resid"].abs().mean(),
                   "mape": (g["resid"].abs() / g["observed"].replace(0, np.nan).abs()).mean() * 100,
                   "resid_to_obs": (
                       g.loc[g["resid"].notna(), "resid"].abs().sum() /
                       g.loc[g["resid"].notna(), "observed"].abs().sum()
                   ) * 100
               }))
               .reset_index())
    return summary


# %%
# Check the result
resid_check = residual_summary(decompose_df, period = 'Downtrend (2023-NOW)', category="Industry")
print(resid_check.sort_values("rmse", ascending=False).head(10))



