import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import polars as pl
from functools import wraps
from chordcodex.model import DBConnection

# =========================================
# Decorators (updated with polars)
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
# QueryExecutor with Polars Method
# =========================================
class QueryExecutor:
    def __init__(self, **config):
        self.config = config
        self.conn = None
        if config:
            self.conn = DBConnection(**config)

    def from_env(self, env_path = ".env"):
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

    def as_raw(self, sql_file: str, params=None):
        """Base method - returns raw results (list of dicts)."""
        try:
            sql_path = Path(sql_file)
            if not sql_path.exists():
                raise FileNotFoundError(f"SQL file not found: {sql_file}")
            
            with open(sql_path, 'r') as f:
                query = f.read()

            with self.conn as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall() if cursor.description else []

        except Exception as e:
            raise RuntimeError(f"Query failed: {str(e)}")

    # Pandas DataFrame
    @pandas_format
    def as_pandas(self, sql_file: str, params=None):
        """Return results as pandas DataFrame."""
        return self.as_raw(sql_file, params)

    # Polars DataFrame (replaces numpy array)
    @polars_format
    def as_polars(self, sql_file: str, params=None):
        """Return results as Polars DataFrame."""
        return self.as_raw(sql_file, params)