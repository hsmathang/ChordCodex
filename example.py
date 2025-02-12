from chordcodex.model import FileExecutor, QueryExecutor

file_executor = FileExecutor().from_env()
query_executor = QueryExecutor().from_env()


### AS FILES ###
# Pandas DataFrame
pd_df = file_executor.as_pandas("sql/all.sql")
# Polars Dataframe
pl_df = file_executor.as_polars("sql/head.sql")

print(pd_df)
print(pl_df)


### AS STR ###
query = """
SELECT *
FROM chords
LIMIT 10;
"""
pl_df = query_executor.as_polars(query)
print(pl_df)