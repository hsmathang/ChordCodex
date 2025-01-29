from sqlalchemy import inspect, text
from db_init import get_engine  # Use get_engine to connect to the database
from sqlalchemy.orm import sessionmaker

def get_table_info(engine, table_name):
    """
    Retrieve information about the specified table, including its columns, row count, and sample data.
    """
    inspector = inspect(engine)
    if table_name not in inspector.get_table_names():
        print(f"Table '{table_name}' does not exist.")
        return

    print(f"--- Table: {table_name} ---")

    # Get column details
    print("\nColumns:")
    columns = inspector.get_columns(table_name)
    for column in columns:
        print(f"- {column['name']} ({column['type']})")

    # Get row count
    with engine.connect() as conn:
        row_count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name};")).scalar()
        print(f"\nRow count: {row_count}")

        # Get sample data
        print("\nSample data:")
        sample_data = conn.execute(text(f"SELECT * FROM {table_name} LIMIT 5;")).fetchall()
        if sample_data:
            for row in sample_data:
                print(row)
        else:
            print("No data available.")

if __name__ == "__main__":
    # Get the database engine
    engine = get_engine()

    # Define the table name
    table_name = "chords"

    # Get information about the table
    get_table_info(engine, table_name)
