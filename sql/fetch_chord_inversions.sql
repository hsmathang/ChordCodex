-- ====================================================
-- 🎼 SQL Query: fetch_chord_inversions.sql
-- 📌 Objetivo: Obtener todas las inversiones musicales de acordes de 3 notas.
-- 🔍 Inversiones calculadas según la teoría musical.
-- 🔄 Se extraen todas las versiones ordenadas del mismo acorde.
-- ====================================================

WITH base_chords AS (
    -- Extraemos los acordes filtrados con sus notas ordenadas
    SELECT DISTINCT notes,
           ARRAY[notes[2], notes[3], notes[1]] AS inversion_1, -- 1ra inversión
           ARRAY[notes[3], notes[1], notes[2]] AS inversion_2  -- 2da inversión
    FROM chords
    WHERE n = 3
    AND (interval = ARRAY[4,3]::integer[] OR
         interval = ARRAY[3,4]::integer[] OR
         interval = ARRAY[3,3]::integer[])
    AND notes <@ ARRAY['0','2','4','5','7','9','B']::varchar[]
)

SELECT *
FROM chords
WHERE notes IN (
    SELECT notes FROM base_chords
    UNION
    SELECT inversion_1 FROM base_chords
    UNION
    SELECT inversion_2 FROM base_chords
)
ORDER BY notes, id;
