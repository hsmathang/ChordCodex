import argparse
from chordcodex.model.executor import QueryExecutor

def main(record_number):
    try:
        executor = QueryExecutor().from_env()

        print(f"Executing query to fetch record number {record_number}...")
        # We use OFFSET which is 0-indexed, so we subtract 1
        offset = record_number - 1
        query = f"SELECT * FROM chords ORDER BY id OFFSET {offset} LIMIT 1;"
        result = executor.as_raw(query=query)

        if result:
            print(f"Record number {record_number}:")
            for row in result:
                print(row)
        else:
            print(f"Record number {record_number} not found.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch a specific record from the chords table.")
    parser.add_argument("record_number", type=int, help="The record number to fetch (1-based).")
    args = parser.parse_args()
    main(args.record_number)
