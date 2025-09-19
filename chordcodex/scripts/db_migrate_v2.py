
import os
import sys
import psycopg2
from dotenv import load_dotenv

# SQL commands to fix the primary key issue.
FIX_SQL = """
-- Drop the old, incorrect text-based primary key.
ALTER TABLE chords DROP CONSTRAINT IF EXISTS chords_pkey;

-- Drop the old id column entirely.
ALTER TABLE chords DROP COLUMN IF EXISTS id;

-- Add a new, correct, auto-incrementing integer primary key.
ALTER TABLE chords ADD COLUMN id BIGSERIAL PRIMARY KEY;
"""

def get_db_connection():
    """Establishes and returns a psycopg2 DB connection."""
    load_dotenv()
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}", file=sys.stderr)
        sys.exit(1)

def run_fix():
    """Executes the SQL script to fix the table schema."""
    print("Connecting to database to fix schema...")
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        print("Executing schema fix for 'id' column...")
        cursor.execute(FIX_SQL)
        conn.commit()
        cursor.close()
        print("Schema fix applied successfully. The 'id' column is now BIGSERIAL PRIMARY KEY.")
    except Exception as e:
        print(f"An error occurred during the schema fix: {e}", file=sys.stderr)
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    run_fix()
