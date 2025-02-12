import os
from dotenv import load_dotenv
import pandas as pd
import polars as pl
from functools import wraps
from chordcodex.model import DBConnection

# =========================================
# Decorators (unchanged)
# =========================================
def pandas_format(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        raw_result = func(*args, **kwargs)
        return pd.DataFrame(raw_result)
    return wrapper

def polars_format(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        raw_result = func(*args, **kwargs)
        return pl.DataFrame(raw_result)
    return wrapper

# =========================================
# Base Executor Class
# =========================================
class BaseExecutor:
    def __init__(self, **config):
        self.config = config
        self.conn = None
        if config:
            self.conn = DBConnection(**config)

    def from_env(self, env_path=".env"):
        load_dotenv(env_path)
        self.config = {
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT", "5432")),
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD")
        }
        self.conn = DBConnection(**self.config)
        return self

    def as_raw(self, query, params=None):
        """Execute SQL and return raw results (list of dicts)."""
        try:
            with self.conn as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall() if cursor.description else []
        except Exception as e:
            raise RuntimeError(f"Query failed: {str(e)}")

    @pandas_format
    def as_pandas(self, query, params=None):
        """Return results as pandas DataFrame."""
        return self.as_raw(query, params)

    @polars_format
    def as_polars(self, query, params=None):
        """Return results as Polars DataFrame."""
        return self.as_raw(query, params)

# =========================================
# FileExecutor for SQL Files
# =========================================
class FileExecutor(BaseExecutor):
    def as_raw(self, sql_file: str, params=None):
        """Execute SQL from a file and return raw results."""
        try:
            with open(sql_file, 'r') as f:
                query = f.read()
            return super().as_raw(query, params)
        except Exception as e:
            raise RuntimeError(f"Query failed: {str(e)}")

# =========================================
# QueryExecutor for SQL Strings
# =========================================
class QueryExecutor(BaseExecutor):
    pass
