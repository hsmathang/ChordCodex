
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# SQL to alter the table, adding new columns and constraints.
# This is designed to be idempotent (can be run multiple times without error).
MIGRATION_SQL = """
-- Step 1: Drop the old unique constraint on 'code' if it exists.
ALTER TABLE chords DROP CONSTRAINT IF EXISTS chords_code_key;

-- Step 2: Add new columns required for the new data model.
ALTER TABLE chords
    ADD COLUMN IF NOT EXISTS span_semitones SMALLINT,
    ADD COLUMN IF NOT EXISTS abs_mask_int BIGINT,
    ADD COLUMN IF NOT EXISTS abs_mask_hex CHAR(7),
    ADD COLUMN IF NOT EXISTS notes_abs_json JSONB;

-- Step 3: Add the new UNIQUE constraint on abs_mask_int, which is required for UPSERT.
ALTER TABLE chords DROP CONSTRAINT IF EXISTS uq_abs;
ALTER TABLE chords ADD CONSTRAINT uq_abs UNIQUE (abs_mask_int);

-- Step 4: Add data integrity CHECK constraints to prevent bad data.
ALTER TABLE chords DROP CONSTRAINT IF EXISTS check_root_note;
ALTER TABLE chords ADD CONSTRAINT check_root_note CHECK ((abs_mask_int & 1) = 1);

ALTER TABLE chords DROP CONSTRAINT IF EXISTS check_note_count;
ALTER TABLE chords ADD CONSTRAINT check_note_count CHECK (n BETWEEN 2 AND 10);

ALTER TABLE chords DROP CONSTRAINT IF EXISTS check_span;
ALTER TABLE chords ADD CONSTRAINT check_span CHECK (span_semitones BETWEEN 0 AND 24);

-- Step 5: Set NOT NULL constraints on columns that must always have a value.
-- This is done last to ensure all alterations succeed on an empty table.
ALTER TABLE chords
    ALTER COLUMN code SET NOT NULL,
    ALTER COLUMN span_semitones SET NOT NULL,
    ALTER COLUMN abs_mask_int SET NOT NULL,
    ALTER COLUMN abs_mask_hex SET NOT NULL,
    ALTER COLUMN notes_abs_json SET NOT NULL;
"""

def get_engine(env_file=".env"):
    """Creates and returns a SQLAlchemy engine using connection details from .env."""
    load_dotenv(env_file)
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    name = os.getenv("DB_NAME")
    
    if not all([host, port, user, password, name]):
        raise ValueError("One or more database environment variables are not set. Please check your .env file.")
        
    database_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
    return create_engine(database_url)

def run_migration():
    """Executes the SQL migration script to alter the 'chords' table."""
    print("Connecting to the database...")
    engine = get_engine()
    
    try:
        with engine.connect() as connection:
            print("Initiating transaction to apply schema migration...")
            with connection.begin() as transaction:
                connection.execute(text(MIGRATION_SQL))
            print("Schema migration completed successfully!")
            print("The 'chords' table is now ready for the new data.")

    except Exception as e:
        print(f"An error occurred during migration: {e}")

if __name__ == "__main__":
    run_migration()
