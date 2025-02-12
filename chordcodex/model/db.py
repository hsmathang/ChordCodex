from sqlalchemy import create_engine, Column, String, Integer, ARRAY, Float
from sqlalchemy.orm import declarative_base

# Define the SQLAlchemy base
Base = declarative_base()

# Chord table (no changes from the previous implementation)
class Chord(Base):
    __tablename__ = "chords"
    id = Column(String, primary_key=True)  # String representation of the chord
    n = Column(Integer, nullable=False)  # Number of notes in the chord
    interval = Column(ARRAY(Integer), nullable=False)  # Intervals between notes (not unique)
    notes = Column(ARRAY(String), nullable=False)  # Notes in the chord
    bass = Column(String, nullable=False)  # First note of the chord (bass)
    octave = Column(Integer, nullable=False)  # Octave of the chord
    frequencies = Column(ARRAY(Float), nullable=False)  # Frequencies of the notes
    chroma = Column(ARRAY(Integer), nullable=False)  # Chroma vector
    tag = Column(String, nullable=False)  # Generation tag
    code = Column(String, nullable=True, unique=True)  # Unique chord code

# Names table
class Name(Base):
    __tablename__ = "names"
    id = Column(Integer, primary_key=True, autoincrement=True)  # Unique ID for the name
    interval = Column(ARRAY(Integer), nullable=False, unique=True)  # Interval as a unique identifier
    name = Column(String, nullable=False)  # Name for the interval
