# ChordCodex Data Architecture

## Vision general
ChordCodex es una investigacion aplicada que combina teoria musical con ingenieria de datos para generar, almacenar y analizar acordes polifonicos. Este README resume la arquitectura completa, el modelo matematico, los pipelines de carga y las utilidades que conforman la base de conocimiento.

## Panorama de la arquitectura
1. **Capa de generacion**
   - `chordcodex/scripts/db_fill.py`: motor original que permuta notas de la escala cromatica ("0"-"B") para poblar la tabla `chords` mediante SQLAlchemy ORM.
   - `chordcodex/scripts/db_fill_v2.py`: generador de segunda generacion (ABS) que trabaja con alturas absolutas 0-24, calcula mascaras binarias y usa inserciones masivas con `execute_values`.
2. **Capa de esquema y migraciones**
   - `chordcodex/model/db.py`: definicion SQLAlchemy de los modelos `Chord` y `Name` (version base).
   - `chordcodex/scripts/db_migrate.py`: agrega columnas absolutas (`span_semitones`, `abs_mask_int`, `abs_mask_hex`, `notes_abs_json`) y constraints de integridad.
   - `chordcodex/scripts/db_migrate_v2.py`: reemplaza la PK de texto por `BIGSERIAL` para soportar cargas masivas.
3. **Capa de acceso**
   - `chordcodex/model/connection.py`: administra conexiones `psycopg2` con contexto seguro.
   - `chordcodex/model/executor.py`: ejecutores base (`QueryExecutor`, `FileExecutor`) con salida cruda, pandas o polars.
   - SQL helpers en `sql/` y clientes (`count_chords.py`, `show_head.py`, `sql_client.py`).
4. **Capa de transformacion y analitica**
   - `chordcodex/transformation/mds.py`: algoritmos MDS clasico y en lotes.
   - `chordcodex/transformation/scales.py`: diccionario de escalas y contextos.

## Variables de entorno
El archivo `.env` define la conexion PostgreSQL:
```
DB_HOST=127.0.0.1
DB_PORT=5432
DB_USER=MathMusician
DB_PASSWORD=F1v3N0t3sCh0rds
DB_NAME=ChordCodex
```
Se recomienda crear un entorno virtual (`python -m venv .venv`) e instalar dependencias (`pip install -r requirements.txt`). En hardware sin AVX2 instale `polars-lts-cpu` y actualice `bottleneck` >= 1.3.6.

## Modelo de datos y matematica de columnas
### Tabla `chords`
| Columna | Tipo | Definicion | Derivacion |
| --- | --- | --- | --- |
| `id` | `BIGSERIAL` (tras migracion v2) | Identificador secuencial | Generado por PostgreSQL |
| `n` | `SMALLINT` | Numero de notas (2-10) | `len(notes_abs)` |
| `interval` | `INT[]` | Intervalos consecutivos en semitonos | `notes_abs[i+1] - notes_abs[i]` |
| `notes` | `VARCHAR[]` | Notas relativas en hex 12-TET | `HEX12[pitch % 12]` |
| `bass` | `VARCHAR` | Clase de tono mas grave | `notes[0]` |
| `octave` | `SMALLINT` | Octava de referencia | `4 + floor(notes_abs[0] / 12)` |
| `frequencies` | `FLOAT[]` | Frecuencias absolutas (Hz) | `NOTE_FREQ[pitch % 12] * 2**(octave-4)` |
| `chroma` | `INT[12]` | Vector binario de clases de tono | `1 si pitch % 12 presente` |
| `tag` | `TEXT` o `TEXT[]` | Etiqueta de generacion (`FULL`, `ABS_V2`) | Valor constante por lote |
| `code` | `TEXT UNIQUE` | Identificador relativo concatenado | `"".join(notes)` |
| `span_semitones` | `SMALLINT` | Amplitud del acorde | `notes_abs[-1] - notes_abs[0]` |
| `abs_mask_int` | `BIGINT UNIQUE` | Mascara absoluta | `sum(1 << pitch)` |
| `abs_mask_hex` | `CHAR(7)` | Mascara en hexadecimal | `format(abs_mask_int, "07X")` |
| `notes_abs_json` | `JSONB` | Alturas absolutas | `json.dumps(notes_abs)` |

### Tabla `names`
| Columna | Tipo | Definicion |
| --- | --- | --- |
| `id` | `SERIAL` | Identificador |
| `interval` | `INT[] UNIQUE` | Patron intervalico |
| `name` | `TEXT` | Denominacion teorica |

## Conteo combinatorio oficial
La generacion absoluta fija la raiz en 0 y combina las 24 alturas restantes. Para `k` notas (2 <= k <= 10):
```
C(24, k-1)  # la raiz ya esta incluida
```
| k | C(24, k-1) |
| --- | --- |
| 2 | 24 |
| 3 | 276 |
| 4 | 2,024 |
| 5 | 10,626 |
| 6 | 42,504 |
| 7 | 134,596 |
| 8 | 346,104 |
| 9 | 735,471 |
| 10 | 1,307,504 |
**Total**: 2,579,129 acordes (coincide con `chord_counter.py`).

## Pipelines de carga
### Version original (`db_fill.py`)
- Permuta notas de la escala cromatica; coste factorial.
- Inserta con SQLAlchemy (`bulk_save_objects`) en lotes de 1,000.

### Version absoluta (`db_fill_v2.py`)
- Usa combinaciones de alturas 0-24 para garantizar unicidad.
- Calcula metadatos absolutos y relativos (mascara, frecuencias, cromas, JSON).
- Inserta en lotes grandes con `execute_values ... ON CONFLICT (abs_mask_int) DO NOTHING`.
- Modos: `benchmark-gen`, `benchmark-insert`, `full-run`.

### Migraciones recomendadas
1. `db_migrate.py`: agrega columnas absolutas y constraints (`uq_abs`, `check_root_note`, etc.).
2. `db_migrate_v2.py`: cambia la PK a `BIGSERIAL` para cargas masivas.

## Operaciones y verificacion
### Consultas clave
```
-- Conteo global
SELECT COUNT(*) FROM chords;

-- Conteo por cardinalidad
SELECT n, COUNT(*) FROM chords GROUP BY n ORDER BY n;

-- Duplicados por mascara absoluta
SELECT COUNT(*) - COUNT(DISTINCT abs_mask_int) FROM chords;
```
Resultados verificados en febrero 2025:
- Total de registros: 2,579,129.
- Distribucion por `n`: coincide con la tabla combinatoria.
- Duplicados (`abs_mask_int`): 0.

### Scripts utilitarios
- `count_chords.py`: imprime el total de filas.
- `db_report_temp.py`: muestra tamano fisico y ejemplos por cardinalidad.
- `show_head.py` + `sql/head.sql`: extraen los primeros registros.
- `sql_client.py`: cliente interactivo (`exit` o `\q` para salir).
- `check_env.py`, `smoke_test.py`: validan configuracion y conectividad.

## Conexion remota paso a paso
1. Crear rol de solo lectura:
   ```sql
   CREATE ROLE chord_reader WITH LOGIN PASSWORD 'cambiarme';
   GRANT CONNECT ON DATABASE "ChordCodex" TO chord_reader;
   GRANT USAGE ON SCHEMA public TO chord_reader;
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO chord_reader;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO chord_reader;
   ```
2. Editar `postgresql.conf` (`listen_addresses='*'`) y `pg_hba.conf` para autorizar IPs confiables.
3. Abrir el puerto 5432 en el firewall unicamente para esas IPs.
4. Reiniciar el servicio PostgreSQL.
5. Probar desde otro equipo:
   ```bash
   psql "postgresql://chord_reader:...@HOST:5432/ChordCodex?sslmode=require"
   ```
6. En Google Colab:
   ```python
   !pip install psycopg2-binary
   import psycopg2
   conn = psycopg2.connect(
       host="HOST",
       port=5432,
       dbname="ChordCodex",
       user="chord_reader",
       password="cambiarme",
       sslmode="require"
   )
   cur = conn.cursor()
   cur.execute("SELECT COUNT(*) FROM chords;")
   print(cur.fetchone())
   cur.close(); conn.close()
   ```
7. Cerrar o ajustar reglas de firewall y rotar contrasenas cuando no se use.

## Analitica y transformaciones
- `mds_batches`: aplica Landmark MDS en lotes para datasets grandes.
- `mds_classic`: MDS exacto o SMACOF para conjuntos pequenos.
- `SCALES_DICTIONARY`: tabla de lookup para mapear escalas a contextos armonicos.

## Roadmap sugerido
- Alinear el modelo ORM (`chordcodex/model/db.py`) con el esquema migrado (tipos y columnas absolutas).
- Documentar directamente en docstrings los scripts v2.
- Automatizar pruebas de conteo y duplicados en CI.
- Publicar datasets derivados (CSV/Parquet) para consumo rapido en Colab.

## Referencia rapida
```
# Inicializar base
python chordcodex/scripts/db_init.py
python chordcodex/scripts/db_migrate.py
python chordcodex/scripts/db_migrate_v2.py

# Cargar acordes (full run)
python chordcodex/scripts/db_fill_v2.py --mode full-run --batch-size 20000

# Validar conteos
python count_chords.py
python chordcodex/scripts/chord_counter.py
```

---
Este README sintetiza la arquitectura completa del proyecto y documenta las rutas v2 (migraciones, cargas y utilidades) creadas para garantizar una base de datos exhaustiva y verificable de acordes.
