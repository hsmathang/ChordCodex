SCALES_DICTIONARY = {
    "Alterada": {
        "name": "Alterada / Super Locrio",
        "num_notes": 7,
        "semitone_formula": [0, 1, 3, 4, 6, 8, 10],
        "degree_formula": "1, b2, b3, b4(3), b5, b6, b7",
        "context": "Escala principal para acordes V7alt en jazz. Contiene todas las alteraciones: b9, #9, b5(#11), #5(b13). 7º modo de la Menor Melódica."
    },
    "Bebop Dominante": {
        "name": "Bebop Dominante",
        "num_notes": 8,
        "semitone_formula": [0, 2, 4, 5, 7, 9, 10, 11],
        "degree_formula": "1, 2, 3, 4, 5, 6, b7, 7",
        "context": "Escala Mixolidia con un 7º grado mayor cromático añadido para alinear los tonos del acorde con los tiempos fuertes en el jazz."
    },
    "Bebop Mayor": {
        "name": "Bebop Mayor",
        "num_notes": 8,
        "semitone_formula": [0, 2, 4, 5, 7, 8, 9, 11],
        "degree_formula": "1, 2, 3, 4, 5, #5, 6, 7",
        "context": "Escala Mayor con un #5 cromático añadido para el fraseo rítmico del bebop."
    },
    "Bebop Menor (Dórica)": {
        "name": "Bebop Menor (Dórica)",
        "num_notes": 8,
        "semitone_formula": [0, 2, 3, 5, 7, 9, 10, 11],
        "degree_formula": "1, 2, b3, 4, 5, 6, b7, 7",
        "context": "Escala Dórica con un 7º grado mayor cromático añadido."
    },
    "Blues Mayor": {
        "name": "Blues Mayor",
        "num_notes": 6,
        "semitone_formula": [0, 2, 3, 4, 7, 9],
        "degree_formula": "1, 2, b3, 3, 5, 6",
        "context": "Pentatónica Mayor con una b3 añadida. Captura la tensión entre la melodía menor y la armonía mayor."
    },
    "Blues Menor": {
        "name": "Blues Menor",
        "num_notes": 6,
        "semitone_formula": [0, 3, 5, 6, 7, 10],
        "degree_formula": "1, b3, 4, b5, 5, b7",
        "context": "Pentatónica Menor con una b5 añadida. La escala de blues más común para la improvisación."
    },
    "China": {
        "name": "China",
        "num_notes": 5,
        "semitone_formula": [0, 4, 6, 7, 11],
        "degree_formula": "1, 3, #4, 5, 7",
        "context": "Escala pentatónica sintética con grandes saltos, a veces utilizada en la improvisación de jazz."
    },
    "Disminuida (Semitono-Tono)": {
        "name": "Disminuida (Semitono-Tono)",
        "num_notes": 8,
        "semitone_formula": [0, 1, 3, 4, 6, 7, 9, 10],
        "degree_formula": "1, b2, b3, 3, #4, 5, 6, b7",
        "context": "Escala simétrica para acordes V7. Genera tensiones b9, #9 y #11."
    },
    "Disminuida (Tono-Semitono)": {
        "name": "Disminuida (Tono-Semitono)",
        "num_notes": 8,
        "semitone_formula": [0, 2, 3, 5, 6, 8, 9, 11],
        "degree_formula": "1, 2, b3, 4, b5, b6, 6, 7",
        "context": "Escala simétrica para acordes de séptima disminuida (dim7)."
    },
    "Dominante Frigio": {
        "name": "Dominante Frigio",
        "num_notes": 7,
        "semitone_formula": [0, 1, 4, 5, 7, 8, 10],
        "degree_formula": "1, b2, 3, 4, 5, b6, b7",
        "context": "5º modo de la Menor Armónica. Para acordes V7(b9, b13). Sonido exótico, español/de Oriente Medio. Idéntica al Maqam Hijaz."
    },
    "Dórica": {
        "name": "Dórica",
        "num_notes": 7,
        "semitone_formula": [0, 2, 3, 5, 7, 9, 10],
        "degree_formula": "1, 2, b3, 4, 5, 6, b7",
        "context": "Modo menor con una 6ª mayor. Sonido brillante y sofisticado, común en jazz, funk y folk."
    },
    "Dórica b2": {
        "name": "Dórica b2",
        "num_notes": 7,
        "semitone_formula": [0, 1, 3, 5, 7, 9, 10],
        "degree_formula": "1, b2, b3, 4, 5, 6, b7",
        "context": "2º modo de la Menor Melódica. Para acordes V7sus(b9)."
    },
    "Eólica (Menor Natural)": {
        "name": "Eólica (Menor Natural)",
        "num_notes": 7,
        "semitone_formula": [0, 2, 3, 5, 7, 8, 10],
        "degree_formula": "1, 2, b3, 4, 5, b6, b7",
        "context": "Tonalidad menor básica. Relativa menor de la escala Mayor."
    },
    "Frigia": {
        "name": "Frigia",
        "num_notes": 7,
        "semitone_formula": [0, 1, 3, 5, 7, 8, 10],
        "degree_formula": "1, b2, b3, 4, 5, b6, b7",
        "context": "Modo menor con una 2ª menor. Sonido oscuro, español/flamenco."
    },
    "Hijaz (Maqam)": {
        "name": "Hijaz (Maqam)",
        "num_notes": 7,
        "semitone_formula": [0, 1, 4, 5, 7, 8, 10],
        "degree_formula": "1, b2, 3, 4, 5, b6, b7",
        "context": "Equivalente en 12-TET del maqam árabe. Idéntica al Dominante Frigio."
    },
    "Hirajoshi": {
        "name": "Hirajoshi",
        "num_notes": 5,
        "semitone_formula": [0, 2, 3, 7, 8],
        "degree_formula": "1, 2, b3, 5, b6",
        "context": "Escala pentatónica japonesa con un carácter melancólico."
    },
    "Insen": {
        "name": "Insen",
        "num_notes": 5,
        "semitone_formula": [0, 1, 5, 7, 10],
        "degree_formula": "1, b2, 4, 5, b7",
        "context": "Escala pentatónica japonesa utilizada en la afinación del koto."
    },
    "Iwato": {
        "name": "Iwato",
        "num_notes": 5,
        "semitone_formula": [0, 1, 5, 6, 10],
        "degree_formula": "1, b2, 4, b5, b7",
        "context": "Escala pentatónica japonesa oscura y tensa."
    },
    "Jónica (Mayor)": {
        "name": "Jónica (Mayor)",
        "num_notes": 7,
        "semitone_formula": [0, 2, 4, 5, 7, 9, 11],
        "degree_formula": "1, 2, 3, 4, 5, 6, 7",
        "context": "La escala mayor estándar, punto de referencia de la armonía occidental."
    },
    "Kurd (Maqam)": {
        "name": "Kurd (Maqam)",
        "num_notes": 7,
        "semitone_formula": [0, 1, 3, 5, 7, 8, 10],
        "degree_formula": "1, b2, b3, 4, 5, b6, b7",
        "context": "Equivalente en 12-TET del maqam árabe. Idéntica al modo Frigio."
    },
    "Lidia": {
        "name": "Lidia",
        "num_notes": 7,
        "semitone_formula": [0, 2, 4, 6, 7, 9, 11],
        "degree_formula": "1, 2, 3, #4, 5, 6, 7",
        "context": "Modo mayor con una 4ª aumentada. Sonido brillante, etéreo, común en bandas sonoras."
    },
    "Lidia Aumentada": {
        "name": "Lidia Aumentada",
        "num_notes": 7,
        "semitone_formula": [0, 2, 4, 6, 8, 9, 11],
        "degree_formula": "1, 2, 3, #4, #5, 6, 7",
        "context": "3er modo de la Menor Melódica. Para acordes maj7(#5)."
    },
    "Lidia Dominante": {
        "name": "Lidia Dominante",
        "num_notes": 7,
        "semitone_formula": [0, 2, 4, 6, 7, 9, 10],
        "degree_formula": "1, 2, 3, #4, 5, 6, b7",
        "context": "4º modo de la Menor Melódica. Para acordes V7(#11)."
    },
    "Locria": {
        "name": "Locria",
        "num_notes": 7,
        "semitone_formula": [0, 1, 3, 5, 6, 8, 10],
        "degree_formula": "1, b2, b3, 4, b5, b6, b7",
        "context": "Modo con una 5ª disminuida. Muy disonante e inestable."
    },
    "Locria #2": {
        "name": "Locria #2",
        "num_notes": 7,
        "semitone_formula": [0, 2, 3, 5, 6, 8, 10],
        "degree_formula": "1, 2, b3, 4, b5, b6, b7",
        "context": "6º modo de la Menor Melódica. Para acordes m7b5 (semidisminuidos)."
    },
    "Mayor Doble Armónica": {
        "name": "Mayor Doble Armónica",
        "num_notes": 7,
        "semitone_formula": [0, 1, 4, 5, 7, 8, 11],
        "degree_formula": "1, b2, 3, 4, 5, b6, 7",
        "context": "Escala sintética con dos segundas aumentadas. Sonido muy exótico."
    },
    "Menor Armónica": {
        "name": "Menor Armónica",
        "num_notes": 7,
        "semitone_formula": [0, 2, 3, 5, 7, 8, 11],
        "degree_formula": "1, 2, b3, 4, 5, b6, 7",
        "context": "Menor Natural con una 7ª mayor para crear un acorde V7."
    },
    "Menor Melódica (Jazz)": {
        "name": "Menor Melódica (Jazz)",
        "num_notes": 7,
        "semitone_formula": [0, 2, 3, 5, 7, 9, 11],
        "degree_formula": "1, 2, b3, 4, 5, 6, 7",
        "context": "Menor Natural con 6ª y 7ª mayores. Escala parental clave en el jazz."
    },
    "Mixolidia": {
        "name": "Mixolidia",
        "num_notes": 7,
        "semitone_formula": [0, 2, 4, 5, 7, 9, 10],
        "degree_formula": "1, 2, 3, 4, 5, 6, b7",
        "context": "Modo mayor con una 7ª menor. Sonido de dominante, blues y rock."
    },
    "Mixolidia b6": {
        "name": "Mixolidia b6",
        "num_notes": 7,
        "semitone_formula": [0, 2, 4, 5, 7, 8, 10],
        "degree_formula": "1, 2, 3, 4, 5, b6, b7",
        "context": "5º modo de la Menor Melódica. Para acordes V7(b13)."
    },
    "Nahawand (Maqam)": {
        "name": "Nahawand (Maqam)",
        "num_notes": 7,
        "semitone_formula": [0, 2, 3, 5, 7, 8, 11],
        "degree_formula": "1, 2, b3, 4, 5, b6, 7",
        "context": "Equivalente en 12-TET del maqam árabe. Idéntica a la Menor Armónica."
    },
    "Pentatónica Mayor": {
        "name": "Pentatónica Mayor",
        "num_notes": 5,
        "semitone_formula": [0, 2, 4, 7, 9],
        "degree_formula": "1, 2, 3, 5, 6",
        "context": "Escala sin semitonos. Sonido abierto, alegre y consonante. Común en la música folclórica y popular."
    },
    "Pentatónica Menor": {
        "name": "Pentatónica Menor",
        "num_notes": 5,
        "semitone_formula": [0, 3, 5, 7, 10],
        "degree_formula": "1, b3, 4, 5, b7",
        "context": "Escala sin semitonos. Sonido melancólico. Fundamental en el rock y el blues."
    },
    "Prometeo / Mística": {
        "name": "Prometeo / Mística",
        "num_notes": 6,
        "semitone_formula": [0, 2, 4, 6, 9, 10],
        "degree_formula": "1, 2, 3, #4, 6, b7",
        "context": "Escala sintética hexatónica asociada a Scriabin. Sonido ambiguo y tenso."
    },
    "Tonos Enteros": {
        "name": "Tonos Enteros",
        "num_notes": 6,
        "semitone_formula": [0, 2, 4, 6, 8, 10],
        "degree_formula": "1, 2, 3, #4, #5, b7",
        "context": "Escala simétrica. Sonido onírico y sin resolver. Asociada a acordes aumentados."
    },
    "Yo": {
        "name": "Yo",
        "num_notes": 5,
        "semitone_formula": [0, 2, 5, 7, 9],
        "degree_formula": "1, 2, 4, 5, 6",
        "context": "Escala pentatónica japonesa. Sonido brillante y abierto, sin terceras."
    }
}
