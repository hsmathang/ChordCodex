from chordcodex.model.executor import QueryExecutor

def main():
    try:
        # Instantiate the executor and load config from .env
        executor = QueryExecutor().from_env()

        # Execute the count query
        print("Executing query to count records in 'chords' table...")
        result = executor.as_raw(query="SELECT COUNT(*) FROM chords;")

        # Print the results
        if result:
            # The count is in the first (and only) row of the result
            count = result[0]['count']
            print(f"The 'chords' table currently contains {count} records.")
        else:
            print("Could not determine the number of records.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
