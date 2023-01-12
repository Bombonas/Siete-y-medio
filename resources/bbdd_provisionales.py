cartas = {
    "O01": {"literal": "As de Oros", "value": 1, "priority": 4, "realValue": 1},
    "O02": {"literal": "Dos de Oros", "value": 2, "priority": 4, "realValue": 2},
    "O03": {"literal": "Tres de Oros", "value": 3, "priority": 4, "realValue": 3},
    "O04": {"literal": "Cuatro de Oros", "value": 4, "priority": 4, "realValue": 4},
    "O05": {"literal": "Cinco de Oros", "value": 5, "priority": 4, "realValue": 5},
    "O06": {"literal": "Seis de Oros", "value": 6, "priority": 4, "realValue": 6},
    "O07": {"literal": "Siete de Oros", "value": 7, "priority": 4, "realValue": 7},
    "O08": {"literal": "Ocho de Oros", "value": 8, "priority": 4, "realValue": 0.5},
    "O09": {"literal": "Nueve de Oros", "value": 9, "priority": 4, "realValue": 0.5},
    "O10": {"literal": "Sota de Oros", "value": 10, "priority": 4, "realValue": 0.5},
    "O11": {"literal": "Caballo de Oros", "value": 11, "priority": 4, "realValue": 0.5},
    "O12": {"literal": "Rey de Oros", "value": 12, "priority": 4, "realValue": 0.5},

    "C01": {"literal": "As de Copas", "value": 1, "priority": 3, "realValue": 1},
    "C02": {"literal": "Dos de Copas", "value": 2, "priority": 3, "realValue": 2},
    "C03": {"literal": "Tres de Copas", "value": 3, "priority": 3, "realValue": 3},
    "C04": {"literal": "Cuatro de Copas", "value": 4, "priority": 3, "realValue": 4},
    "C05": {"literal": "Cinco de Copas", "value": 5, "priority": 3, "realValue": 5},
    "C06": {"literal": "Seis de Copas", "value": 6, "priority": 3, "realValue": 6},
    "C07": {"literal": "Siete de Copas", "value": 7, "priority": 3, "realValue": 7},
    "C08": {"literal": "Ocho de Copas", "value": 8, "priority": 3, "realValue": 0.5},
    "C09": {"literal": "Nueve de Copas", "value": 9, "priority": 3, "realValue": 0.5},
    "C10": {"literal": "Sota de Copas", "value": 10, "priority": 3, "realValue": 0.5},
    "C11": {"literal": "Caballo de Copas", "value": 11, "priority": 3, "realValue": 0.5},
    "C12": {"literal": "Rey de Copas", "value": 12, "priority": 3, "realValue": 0.5},

    "E01": {"literal": "As de Espadas", "value": 1, "priority": 2, "realValue": 1},
    "E02": {"literal": "Dos de Espadas", "value": 2, "priority": 2, "realValue": 2},
    "E03": {"literal": "Tres de Espadas", "value": 3, "priority": 2, "realValue": 3},
    "E04": {"literal": "Cuatro de Espadas", "value": 4, "priority": 2, "realValue": 4},
    "E05": {"literal": "Cinco de Espadas", "value": 5, "priority": 2, "realValue": 5},
    "E06": {"literal": "Seis de Espadas", "value": 6, "priority": 2, "realValue": 6},
    "E07": {"literal": "Siete de Espadas", "value": 7, "priority": 2, "realValue": 7},
    "E08": {"literal": "Ocho de Espadas", "value": 8, "priority": 2, "realValue": 0.5},
    "E09": {"literal": "Nueve de Espadas", "value": 9, "priority": 2, "realValue": 0.5},
    "E10": {"literal": "Sota de Espadas", "value": 10, "priority": 2, "realValue": 0.5},
    "E11": {"literal": "Caballo de Espadas", "value": 11, "priority": 2, "realValue": 0.5},
    "E12": {"literal": "Rey de Espadas", "value": 12, "priority": 2, "realValue": 0.5},

    "B01": {"literal": "As de Bastos", "value": 1, "priority": 1, "realValue": 1},
    "B02": {"literal": "Dos de Bastos", "value": 2, "priority": 1, "realValue": 2},
    "B03": {"literal": "Tres de Bastos", "value": 3, "priority": 1, "realValue": 3},
    "B04": {"literal": "Cuatro de Bastos", "value": 4, "priority": 1, "realValue": 4},
    "B05": {"literal": "Cinco de Bastos", "value": 5, "priority": 1, "realValue": 5},
    "B06": {"literal": "Seis de Bastos", "value": 6, "priority": 1, "realValue": 6},
    "B07": {"literal": "Siete de Bastos", "value": 7, "priority": 1, "realValue": 7},
    "B08": {"literal": "Ocho de Bastos", "value": 8, "priority": 1, "realValue": 0.5},
    "B09": {"literal": "Nueve de Bastos", "value": 9, "priority": 1, "realValue": 0.5},
    "B10": {"literal": "Sota de Bastos", "value": 10, "priority": 1, "realValue": 0.5},
    "B11": {"literal": "Caballo de Bastos", "value": 11, "priority": 1, "realValue": 0.5},
    "B12": {"literal": "Rey de Bastos", "value": 12, "priority": 1, "realValue": 0.5},
}

players = { "11115555A":
                { "name":"Mario", "human":True, "bank":False, "initialCard":"", "priority":0, "type":40,
                  "bet":4, "points":0, "cards":[], "roundPoints":0},
            "22225555A":
                { "name":"Pedro", "human":True, "bank":False, "initialCard":"", "priority":0, "type":40,
                  "bet":4, "points":0, "cards":[], "roundPoints":0},
            "34343434H":
                { "name":"Bot1", "human":False, "bank":False, "initialCard":"", "priority":0, "type":30,
                  "bet":4, "points":0, "cards":[], "roundPoints":0},
            "11111111A":
                { "name":"Bot2", "human":False, "bank":False, "initialCard":"", "priority":0, "type":50,
                  "bet":4, "points":0, "cards":[], "roundPoints":0}
            }

letrasDni = ["T", "R", "W", "A", "G", "M", "Y", "F", "P", "D", "X", "B", "N",
             "J", "Z", "S", "Q", "V", "H", "L", "C", "K", "E"]

contextGame = {"maxRounds": 5}