import os
import sys
import time
import json
import argparse
import psycopg2
from itertools import combinations
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# --- Constantes y Configuración ---

# Rango de notas a combinar (la nota 0 es la raíz obligatoria)
PITCH_RANGE = range(1, 25)
MIN_NOTES = 2
MAX_NOTES = 10
TAG = "ABS_V2"

# Mapeo de notas a frecuencias base (para la octava 4)
NOTE_FREQUENCIES = {
    0: 261.63, 1: 277.18, 2: 293.66, 3: 311.13, 4: 329.63, 5: 349.23,
    6: 369.99, 7: 391.99, 8: 415.30, 9: 440.00, 10: 466.16, 11: 493.88
}
HEX12 = "0123456789AB"

# --- Funciones de Conexión y Cálculo ---

def get_db_connection():
    """Establece y devuelve una conexión a la BD usando psycopg2."""
    load_dotenv()
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}", file=sys.stderr)
        sys.exit(1)

def calculate_row(notes_abs):
    """
    Calcula todos los campos para una fila de la BD a partir de una lista de alturas absolutas.
    Devuelve una tupla en el orden correcto para la inserción.
    """
    # Campos nuevos
    n = len(notes_abs)
    span_semitones = notes_abs[-1] - notes_abs[0]
    code = "".join([HEX12[note % 12] for note in notes_abs])
    
    abs_mask_int = 0
    for note in notes_abs:
        abs_mask_int |= (1 << note)
    
    abs_mask_hex = format(abs_mask_int, '07X')
    notes_abs_json = json.dumps(notes_abs)

    # Campos antiguos (con la nueva lógica acordada)
    pitch_classes = [str(note % 12) for note in notes_abs]
    bass = str(notes_abs[0] % 12)
    
    intervals = [(notes_abs[i+1] - notes_abs[i]) for i in range(n - 1)]
    
    octaves = [4 + (note // 12) for note in notes_abs]
    
    frequencies = [NOTE_FREQUENCIES[note % 12] * (2 ** ((4 + (note // 12)) - 4)) for note in notes_abs]

    chroma = [0] * 12
    for note in notes_abs:
        chroma[note % 12] = 1

    # El ID de la tabla 'chords' original era un string, lo dejamos vacío
    # ya que el nuevo id es un BIGSERIAL manejado por la BD.
    # El tag en la tabla original era un string, no un array.
    return (
        n, intervals, pitch_classes, bass, octaves[0], frequencies, chroma, TAG, code,
        span_semitones, abs_mask_int, abs_mask_hex, notes_abs_json
    )

def chord_generator():
    """Generador que produce todas las combinaciones de acordes posibles."""
    for k in range(MIN_NOTES, MAX_NOTES + 1):
        # k-1 porque la nota 0 siempre está incluida
        for combo in combinations(PITCH_RANGE, k - 1):
            # Añadir la raíz 0 y ordenar
            yield sorted((0,) + combo)

# --- Lógica de Ejecución ---

def run_generation_benchmark(limit):
    """Mide la velocidad de generación de datos en memoria."""
    print(f"Iniciando benchmark de GENERACIÓN para {limit} acordes...")
    start_time = time.time()
    
    count = 0
    for notes_abs in chord_generator():
        if count >= limit:
            break
        _ = calculate_row(notes_abs)
        count += 1
        
    end_time = time.time()
    duration = end_time - start_time
    rate = count / duration if duration > 0 else float('inf')
    
    print(f"Generados {count} acordes en {duration:.2f} segundos.")
    print(f"Velocidad de generación: {rate:,.0f} acordes/segundo.")
    return rate

def run_insertion_benchmark(limit, batch_size):
    """Mide la velocidad de inserción de datos en la base de datos."""
    print(f"Iniciando benchmark de INSERCIÓN para {limit} acordes (lotes de {batch_size})...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Activar modo de alto rendimiento
    cursor.execute("SET synchronous_commit = off;")
    
    sql_insert = """
        INSERT INTO chords (
            n, interval, notes, bass, octave, frequencies, chroma, tag, code,
            span_semitones, abs_mask_int, abs_mask_hex, notes_abs_json
        ) VALUES %s ON CONFLICT (abs_mask_int) DO NOTHING;
    """
    
    start_time = time.time()
    
    batch = []
    count = 0
    total_inserted = 0
    
    for notes_abs in chord_generator():
        if count >= limit:
            break
        
        batch.append(calculate_row(notes_abs))
        count += 1
        
        if len(batch) >= batch_size:
            inserted_count = execute_values(cursor, sql_insert, batch, page_size=batch_size)
            total_inserted += cursor.rowcount
            conn.commit()
            batch = []
            print(f"  ... {total_inserted:,.0f} acordes insertados.", end='\r')

    if batch:
        execute_values(cursor, sql_insert, batch, page_size=len(batch))
        total_inserted += cursor.rowcount
        conn.commit()

    # Restaurar configuración
    cursor.execute("SET synchronous_commit = on;")
    
    end_time = time.time()
    duration = end_time - start_time
    rate = total_inserted / duration if duration > 0 else float('inf')
    
    print(f"\nInsertados {total_inserted} acordes en {duration:.2f} segundos.")
    print(f"Velocidad de inserción: {rate:,.0f} acordes/segundo.")
    
    cursor.close()
    conn.close()
    return rate

def run_full_process(batch_size):
    """Ejecuta el proceso completo de generación e inserción sin límite."""
    print(f"Iniciando proceso de carga COMPLETA (lotes de {batch_size})...")
    
    try:
        from tqdm import tqdm
    except ImportError:
        print("La librería 'tqdm' no está instalada. No se mostrará la barra de progreso.", file=sys.stderr)
        print("Puede instalarla con: pip install tqdm", file=sys.stderr)
        # Dummy tqdm if not installed
        class tqdm:
            def __init__(self, *args, **kwargs):
                pass
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def update(self, n=1):
                pass
            def set_postfix(self, **kwargs):
                pass

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Activar modo de alto rendimiento
    cursor.execute("SET synchronous_commit = off;")
    
    sql_insert = """
        INSERT INTO chords (
            n, interval, notes, bass, octave, frequencies, chroma, tag, code,
            span_semitones, abs_mask_int, abs_mask_hex, notes_abs_json
        ) VALUES %s ON CONFLICT (abs_mask_int) DO NOTHING;
    """
    
    start_time = time.time()
    
    batch = []
    total_inserted = 0
    
    print("Calculando el número total de acordes a generar (esto puede tardar un momento)...")
    total_chords = sum(1 for _ in chord_generator())
    print(f"Se generarán e insertarán hasta {total_chords:,} acordes.")

    generator = chord_generator()
    
    with tqdm(total=total_chords, desc="Insertando acordes", unit="acorde") as pbar:
        for notes_abs in generator:
            batch.append(calculate_row(notes_abs))
            
            if len(batch) >= batch_size:
                execute_values(cursor, sql_insert, batch, page_size=batch_size)
                inserted_this_batch = cursor.rowcount
                total_inserted += inserted_this_batch
                pbar.update(len(batch))
                pbar.set_postfix(insertados=f'{total_inserted:,}')
                conn.commit()
                batch = []

    if batch:
        execute_values(cursor, sql_insert, batch, page_size=len(batch))
        inserted_this_batch = cursor.rowcount
        total_inserted += inserted_this_batch
        pbar.update(len(batch))
        pbar.set_postfix(insertados=f'{total_inserted:,}')
        conn.commit()

    # Restaurar configuración
    cursor.execute("SET synchronous_commit = on;")
    
    end_time = time.time()
    duration = end_time - start_time
    rate = total_inserted / duration if duration > 0 else float('inf')
    
    print(f"\nProceso completado. Insertados {total_inserted:,} acordes nuevos en {duration:.2f} segundos.")
    print(f"Velocidad de inserción: {rate:,.0f} acordes/segundo.")
    
    cursor.close()
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador y poblador de la base de datos de acordes.")
    parser.add_argument(
        '--mode',
        choices=['benchmark-gen', 'benchmark-insert', 'full-run'],
        required=True,
        help="El modo de operación."
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=200000,
        help="Número de acordes a procesar en los benchmarks."
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=20000,
        help="Tamaño de los lotes para la inserción en la base de datos."
    )
    
    args = parser.parse_args()
    
    if args.mode == 'benchmark-gen':
        run_generation_benchmark(args.limit)
    elif args.mode == 'benchmark-insert':
        # Usar el límite del argumento para la inserción
        run_insertion_benchmark(args.limit, args.batch_size)
    elif args.mode == 'full-run':
        run_full_process(args.batch_size)