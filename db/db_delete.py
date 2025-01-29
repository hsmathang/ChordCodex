import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get database connection parameters from environment variables
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DB_NAME = os.getenv("NAME")

# Function to delete and recreate the database
def reset_database():
    try:
        # Connect to PostgreSQL (initial connection is to the default "postgres" database)
        connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            dbname="postgres"  # Default database
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # Allow database-level commands
        cursor = connection.cursor()

        # Drop the database if it exists
        cursor.execute(f"DROP DATABASE IF EXISTS \"{DB_NAME}\";")
        print(f"Database '{DB_NAME}' deleted successfully.")

        # Recreate the database
        cursor.execute(f"CREATE DATABASE \"{DB_NAME}\";")
        print(f"Database '{DB_NAME}' created successfully.")

    except Exception as e:
        print(f"Error resetting database: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    reset_database()
