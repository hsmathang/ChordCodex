import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_config():
    """Load and validate database configuration from environment variables."""
    config = {
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD")
    }
    
    # Validate all required fields are present
    for key, value in config.items():
        if value is None:
            raise EnvironmentError(f"Missing required environment variable: POSTGRES_{key.upper()}")
    
    return config