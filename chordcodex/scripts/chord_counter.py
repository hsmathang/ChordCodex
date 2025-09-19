import time
import math

# --- PARÁMETROS DE CONFIGURACIÓN ---
# Estos parámetros definen las restricciones para el conteo.

# El número máximo de notas que puede tener un acorde.
MAX_NOTES_IN_CHORD = 10

# La amplitud máxima (span) en semitonos. Un valor de 24 significa que tenemos
# 25 alturas de nota disponibles (de 0 a 24 inclusive).
MAX_SEMITONE_SPAN = 24

def calculate_possible_chords():
    """
    Calcula el número de acordes posibles basándose en un modelo combinatorio.

    El modelo asume:
    1. Un universo de N+1 alturas de nota disponibles (0 a N).
    2. Todos los acordes deben incluir la nota 0 (la raíz).
    3. Un acorde es un subconjunto de notas de este universo.

    La fórmula es: Sumatoria de C(N, k-1) para k desde 2 hasta MAX_NOTES,
    donde N es el número de notas disponibles además de la raíz.
    """
    print("--- Calculando el Número de Acordes Posibles (Modelo Corregido) ---")
    print("Modelo: Combinaciones de un conjunto de alturas de nota disponibles.")
    print(f"Restricciones:")
    print(f"  - Universo de alturas: {MAX_SEMITONE_SPAN + 1} notas (de 0 a {MAX_SEMITONE_SPAN}).")
    print(f"  - Nota raíz: Siempre se incluye la nota 0 (Do).")
    print(f"  - Tamaño del acorde (k): de 2 a {MAX_NOTES_IN_CHORD} notas.")
    print("-" * 60)

    # El número de notas disponibles para elegir, ADEMÁS de la raíz que ya está fija.
    available_notes_pool_size = MAX_SEMITONE_SPAN

    grand_total = 0
    chords_by_size = {}

    # Iteramos para cada tamaño de acorde 'k'.
    for k in range(2, MAX_NOTES_IN_CHORD + 1):
        # Para un acorde de tamaño 'k', ya hemos elegido la raíz (nota 0).
        # Necesitamos elegir las 'k - 1' notas restantes.
        notes_to_choose = k - 1

        # Usamos la fórmula de combinatoria "n sobre r": C(n, r)
        # n = available_notes_pool_size
        # r = notes_to_choose
        if notes_to_choose > available_notes_pool_size:
            count_for_k = 0
        else:
            count_for_k = math.comb(available_notes_pool_size, notes_to_choose)
        
        chords_by_size[k] = count_for_k
        grand_total += count_for_k

    print("Resultados del Conteo:")
    for size, count in chords_by_size.items():
        print(f"  - Acordes de {size} notas: {count:,}")
    print("-" * 60)
    print(f"NÚMERO TOTAL DE ACORDES POSIBLES: {grand_total:,}")
    print("-" * 60)


if __name__ == "__main__":
    start_time = time.time()
    calculate_possible_chords()
    end_time = time.time()
    print(f"Cálculo completado en {end_time - start_time:.8f} segundos.")

