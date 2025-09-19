import os
from dotenv import load_dotenv

def check_environment_variables():
    """
    Loads variables from .env and prints the database connection details.
    """
    print("Loading environment variables from .env file...")
    was_loaded = load_dotenv(".env")
    
    if not was_loaded:
        print("\n--- WARNING ---")
        print("Could not find a .env file in the root directory.")
        print("-----------------\n")
        return

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    user = os.getenv("DB_USER")
    name = os.getenv("DB_NAME")
    
    print("\n--- Database Connection Parameters ---")
    print(f"  Host:     {host}")
    print(f"  Port:     {port}")
    print(f"  Database: {name}")
    print(f"  User:     {user}")
    print("-------------------------------------\n")
    print("Please verify that these are the EXACT parameters for the database where you granted permissions.")
    print("Pay close attention to hostname (e.g., 'localhost' vs '127.0.0.1') and case-sensitivity in the username.")

if __name__ == "__main__":
    check_environment_variables()
