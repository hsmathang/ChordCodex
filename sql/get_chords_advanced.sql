SELECT * FROM chords
WHERE 
    (%s IS NULL OR intervals = ANY(%s::integer[])) AND
    (%s IS NULL OR bass = %s) AND
    (%s IS NULL OR octave = %s) AND
    (%s IS NULL OR tag = %s);
