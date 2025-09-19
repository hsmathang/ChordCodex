import asyncio
from chordcodex.model.executor import FileExecutor

def main():
    try:
        # Instantiate the executor and load config from .env
        executor = FileExecutor().from_env()

        # Execute the query from the SQL file
        print("Executing query from sql/head.sql...")
        result = executor.as_raw(sql_file="sql/head.sql")

        # Print the results
        if result:
            print("First 10 records from the 'chords' table:")
            for row in result:
                print(row)
        else:
            print("No records found or query returned empty.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
