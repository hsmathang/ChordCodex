import psycopg2
from psycopg2.extras import RealDictCursor
from config.db_config import get_db_config

class DBConnection:
    """Context manager for PostgreSQL connections using env vars."""
    def __enter__(self):
        self.conn = psycopg2.connect(
            **get_db_config(),
            cursor_factory=RealDictCursor
        )
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.cursor.close()
        self.conn.close()