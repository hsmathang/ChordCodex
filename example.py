from model import QueryExecutor

executor = QueryExecutor().from_env()

# Pandas DataFrame
pd_df = executor.as_pandas("sql/all.sql")

# Polars Dataframe
pl_df = executor.as_polars("sql/head.sql")

print(pd_df)
print(pl_df)