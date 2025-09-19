from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..model.db import Chord, Base  # Import the Chord model and Base from your model file
import os
from dotenv import load_dotenv

def get_engine(env_file: str=".env"):
    """
    Create and return a SQLAlchemy engine using the connection details from .env.
    """
    load_dotenv(env_file)

    HOST = os.getenv("DB_HOST")
    PORT = os.getenv("DB_PORT")
    USER = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASSWORD")
    NAME = os.getenv("DB_NAME")

    if not all([HOST, PORT, USER, PASSWORD, NAME]):
        raise ValueError("One or more database environment variables are not set.")
    
    DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"
    return create_engine(DATABASE_URL, echo=True)

def init_db():
    """
    Initialize the database and create all tables.
    """
    engine = get_engine()  # Get the engine
    Base.metadata.create_all(engine)  # Create tables based on the Base metadata
    print("Database and table initialized!")
    return engine

# Main script to initialize the database
if __name__ == "__main__":
    try:
        init_db()
    except Exception as e:
        print(f"Error initializing the database: {e}")
