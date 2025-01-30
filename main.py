from model import QueryExecutor



# Raw results (list of dictionaries)
raw = QueryExecutor.execute("sql/head.sql")

# Pandas DataFrame
df = QueryExecutor.as_df("sql/head.sql")

# Numpy array
#arr = QueryExecutor.as_array("sql/head.sql")

print(df)