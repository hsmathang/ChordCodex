import os
import sys
from dotenv import load_dotenv
import psycopg2

def interactive_sql_client():
    """
    An interactive command-line client to connect to the PostgreSQL database
    and execute queries.
    """
    load_dotenv()
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()
        print("--- Cliente SQL Interactivo de Python ---")
        print(f"Conectado a la base de datos '{os.getenv('DB_NAME')}' en {os.getenv('DB_HOST')}.")
        print("Escribe tu consulta SQL y presiona Enter. Escribe 'exit' para salir.")

        while True:
            try:
                query_str = input(f"{os.getenv('DB_NAME')}=> ")
                if query_str.strip().lower() in ['\\q', 'exit']:
                    print("Saliendo del cliente SQL.")
                    break
                if not query_str.strip():
                    continue

                cur.execute(query_str)

                if cur.description:
                    col_names = [desc[0] for desc in cur.description]
                    print(" | ".join(col_names))
                    print("-" * (sum(len(n) for n in col_names) + 3 * len(col_names)))
                    
                    rows = cur.fetchall()
                    for row in rows:
                        print(" | ".join(str(item) for item in row))
                    print(f"({len(rows)} rows)")
                else:
                    conn.commit()
                    print(f"OK. {cur.rowcount} filas afectadas.")

            except psycopg2.Error as e:
                print(f"Error de base de datos: {e}", file=sys.stderr)
                conn.rollback()
            except KeyboardInterrupt:
                print("\nSaliendo del cliente SQL.")
                break

    except psycopg2.OperationalError as e:
        print(f"Error de conexión: No se pudo conectar a la base de datos.", file=sys.stderr)
        print(f"Asegúrate de que la base de datos esté en ejecución y que las variables de entorno son correctas.", file=sys.stderr)
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}", file=sys.stderr)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    interactive_sql_client()
