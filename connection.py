import psycopg2
from psycopg2 import sql

# Connection parameters
HOST = "https://machinemindcore.cloud"  # Use "localhost" if running locally
PORT = 5432
DB_NAME = "ChordCodex"
USER = "MathMusician"
PASSWORD = "F1v3N0t3sCh0rds"

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        host=HOST,
        port=PORT,
        database=DB_NAME,
        user=USER,
        password=PASSWORD
    )

    cursor = connection.cursor()
    
    # Execute a test query
    cursor.execute("SELECT COUNT(*) FROM chords;")
    count = cursor.fetchone()[0]
    print(f"Connection successful! Total rows in 'chords': {count}")

except Exception as e:
    print(f"Error: {e}")

finally:
    if connection:
        cursor.close()
        connection.close()
