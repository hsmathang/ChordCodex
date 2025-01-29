from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Chord, Base  # Import the Chord model and Base from your model file
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def get_engine():
    """
    Create and return a SQLAlchemy engine using the connection details from .env.
    """
    HOST = os.environ.get("DB_HOST")
    PORT = os.environ.get("DB_PORT")
    USER = os.environ.get("DB_USER")
    PASSWORD = os.environ.get("DB_PASSWORD")
    NAME = os.environ.get("DB_NAME")
    
    if not all([HOST, PORT, USER, PASSWORD, NAME]):
        raise ValueError("Some database connection variables are missing in .env file.")
    
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
