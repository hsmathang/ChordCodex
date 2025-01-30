from pathlib import Path
import pandas as pd
import numpy as np
from functools import wraps
from model import DBConnection

# =========================================
# Decorators (unchanged)
# =========================================
def pandas_format(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        raw_result = func(*args, **kwargs)
        return pd.DataFrame(raw_result)
    return wrapper

def numpy_format(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        raw_result = func(*args, **kwargs)
        if not raw_result:
            return np.array([])
        return np.array([list(row.values()) for row in raw_result])
    return wrapper

# =========================================
# QueryExecutor with Short Method Names
# =========================================
class QueryExecutor:
    @staticmethod
    def execute(sql_file: str, params=None):
        """Base method - returns raw results (list of dicts)."""
        try:
            sql_path = Path(sql_file)
            if not sql_path.exists():
                raise FileNotFoundError(f"SQL file not found: {sql_file}")
            
            with open(sql_path, 'r') as f:
                query = f.read()

            with DBConnection() as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall() if cursor.description else []

        except Exception as e:
            raise RuntimeError(f"Query failed: {str(e)}")

    # Shortened methods with decorators
    @staticmethod
    @pandas_format
    def as_df(sql_file: str, params=None):
        """Return results as pandas DataFrame."""
        return QueryExecutor.execute(sql_file, params)

    @staticmethod
    @numpy_format
    def as_array(sql_file: str, params=None):
        """Return results as numpy array."""
        return QueryExecutor.execute(sql_file, params)