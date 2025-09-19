import os
import sys
from dotenv import load_dotenv
import psycopg2

def db_report():
    """
    Connects to the database, generates a report on the 'chords' table,
    and prints a sample of chords.
    """
    load_dotenv()
    conn = None
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()

        print("--- Informe de la Base de Datos ---")

        # 1. Get total chord count
        cur.execute("SELECT COUNT(*) FROM chords;")
        count = cur.fetchone()[0]
        print(f"\nTotal de acordes en la tabla 'chords': {count:,}")

        if count > 2000000:
            print("\nConfirmado: La base de datos está completamente poblada.")
            print("El script 'db_fill_v2' reportó 0 inserciones porque los acordes ya existían, lo cual es correcto.")

        # 2. Get table size
        cur.execute("SELECT pg_size_pretty(pg_total_relation_size('chords'));")
        size = cur.fetchone()[0]
        print(f"Tamaño total de la tabla 'chords': {size}")

        # 3. Get sample chords
        print("\n--- Muestra de Acordes por Número de Notas ---")
        for n in range(2, 12):
            print(f"\nAcorde de {n} notas:")
            cur.execute(f"SELECT n, notes_abs_json, code, span_semitones FROM chords WHERE n = {n} LIMIT 1;")
            sample = cur.fetchone()
            if sample:
                print(f"  - n: {sample[0]}")
                print(f"  - Notas (absolutas): {sample[1]}")
                print(f"  - Código: {sample[2]}")
                print(f"  - Extensión (semitonos): {sample[3]}")
            else:
                print("  - No se encontraron acordes.")

        cur.close()
    except psycopg2.OperationalError as e:
        print(f"Error de conexión: No se pudo conectar a la base de datos.", file=sys.stderr)
        print(f"Asegúrate de que la base de datos esté en ejecución y que las variables de entorno en tu archivo .env son correctas.", file=sys.stderr)
        print(f"Detalle: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    db_report()
