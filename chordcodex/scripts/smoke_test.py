# scripts/smoke_test.py
import os
from dotenv import load_dotenv
import psycopg2

# Cargar variables del .env
load_dotenv()

def main():
    # Intentar conectar a PostgreSQL con credenciales del .env
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_NAME"),
        )
        with conn.cursor() as cur:
            cur.execute("SELECT current_database(), version();")
            dbname, version = cur.fetchone()
            print("✅ Conexión exitosa")
            print("   Base de datos:", dbname)
            print("   Versión:", version)
    except Exception as e:
        print("❌ Error de conexión:", e)

if __name__ == "__main__":
    main()
