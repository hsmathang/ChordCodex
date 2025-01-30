from itertools import permutations
from sqlalchemy.orm import sessionmaker
from db_init import Chord, get_engine

# Constants
TAG = "FULL"  # Generation tag
OCTAVE = 4  # Fixed starting octave
MIN_SIZE = 1
MAX_SIZE = 5

CHROMATIC_SCALE = {
    "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "A": 10, "B": 11
}

NOTE_FREQUENCIES = {
    "0": 261.63, "1": 277.18, "2": 293.66, "3": 311.13, "4": 329.63,
    "5": 349.23, "6": 369.99, "7": 391.99, "8": 415.30, "9": 440.00,
    "A": 466.16, "B": 493.88
}

def compute_intervals(notes):
    """Compute intervals between consecutive notes."""
    numeric_notes = [CHROMATIC_SCALE[note] for note in notes]
    intervals = [(numeric_notes[i + 1] - numeric_notes[i]) % 12 for i in range(len(numeric_notes) - 1)]
    return intervals

def compute_frequencies_and_octaves(notes):
    """
    Compute frequencies dynamically based on intervals and adjust octaves.
    The first note is fixed to the starting octave (OCTAVE).
    """
    frequencies = []
    octaves = []

    # Base frequency and octave for the first note
    base_note = notes[0]
    base_frequency = NOTE_FREQUENCIES[base_note] * (2 ** (OCTAVE - 4))
    frequencies.append(base_frequency)
    octaves.append(OCTAVE)

    # Calculate frequencies and octaves for the remaining notes
    current_pitch = CHROMATIC_SCALE[base_note] + OCTAVE * 12
    for note in notes[1:]:
        target_pitch = CHROMATIC_SCALE[note]
        while target_pitch + (octaves[-1] * 12) < current_pitch:
            target_pitch += 12  # Adjust to the next octave
        current_pitch = target_pitch + (octaves[-1] * 12)
        target_octave = current_pitch // 12
        octaves.append(target_octave)
        frequency = NOTE_FREQUENCIES[note] * (2 ** (target_octave - 4))
        frequencies.append(frequency)

    return frequencies, octaves

def compute_chroma(notes):
    """Compute the chroma vector for the chord."""
    chroma = [0] * 12
    for note in notes:
        chroma[CHROMATIC_SCALE[note] % 12] = 1
    return chroma

def lazy_generate_chords(strings, min_size, max_size):
    """Generate chords lazily."""
    for r in range(min_size, max_size + 1):
        for chord_tuple in permutations(strings, r):
            notes = list(chord_tuple)
            code = "".join(notes)  # Concatenate notes to form the code
            chord_id = f"{TAG}_{OCTAVE}-{code}"  # Format ID
            bass = notes[0]  # First note as bass
            intervals = compute_intervals(notes)
            frequencies, octaves = compute_frequencies_and_octaves(notes)
            chroma = compute_chroma(notes)

            yield {
                "id": chord_id,
                "n": r,
                "interval": intervals,
                "notes": notes,
                "bass": bass,
                "octave": OCTAVE,
                "frequencies": frequencies,
                "chroma": chroma,
                "tag": TAG,
                "code": code
            }

def populate_db(engine, strings, min_size, max_size):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        batch_size = 1000
        batch = []
        batch_count = 0

        for chord_data in lazy_generate_chords(strings, min_size, max_size):
            batch.append(Chord(**chord_data))

            if len(batch) >= batch_size:
                session.bulk_save_objects(batch)
                session.commit()
                batch_count += 1
                if batch_count % 10 == 0:  # Print every 10th batch
                    print(f"Inserted {batch_count * batch_size} chords")
                batch = []

        # Insert any remaining chords
        if batch:
            session.bulk_save_objects(batch)
            session.commit()
            print(f"Inserted final batch of {len(batch)} chords")

    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    engine = get_engine()
    strings = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B"]
    populate_db(engine, strings, MIN_SIZE, MAX_SIZE)
    print("Database population complete!")
