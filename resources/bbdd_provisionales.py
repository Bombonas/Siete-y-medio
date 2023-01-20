import mysql.connector

db = mysql.connector.connect(user="MAP", password="2023Proyecto",
                                   host="proyecto1.mysql.database.azure.com",
                                   database="seven_and_half",
                                   port="3306")
cursor = db.cursor()
cartas = {}
cartas1 = {
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

cartas2 = {
    "D01": {"literal": "As de Diamantes", "value": 1, "priority": 4, "realValue": 1},
    "D02": {"literal": "Dos de Diamantes", "value": 2, "priority": 4, "realValue": 2},
    "D03": {"literal": "Tres de Diamantes", "value": 3, "priority": 4, "realValue": 3},
    "D04": {"literal": "Cuatro de Diamantes", "value": 4, "priority": 4, "realValue": 4},
    "D05": {"literal": "Cinco de Diamantes", "value": 5, "priority": 4, "realValue": 5},
    "D06": {"literal": "Seis de Diamantes", "value": 6, "priority": 4, "realValue": 6},
    "D07": {"literal": "Siete de Diamantes", "value": 7, "priority": 4, "realValue": 7},
    "D08": {"literal": "Ocho de Diamantes", "value": 8, "priority": 4, "realValue": 0.5},
    "D09": {"literal": "Nueve de Diamantes", "value": 9, "priority": 4, "realValue": 0.5},
    "D10": {"literal": "J de Diamantes", "value": 10, "priority": 4, "realValue": 0.5},
    "D11": {"literal": "Q de Diamantes", "value": 11, "priority": 4, "realValue": 0.5},
    "D12": {"literal": "K de Diamantes", "value": 12, "priority": 4, "realValue": 0.5},

    "C01": {"literal": "As de Corazones", "value": 1, "priority": 3, "realValue": 1},
    "C02": {"literal": "Dos de Corazones", "value": 2, "priority": 3, "realValue": 2},
    "C03": {"literal": "Tres de Corazones", "value": 3, "priority": 3, "realValue": 3},
    "C04": {"literal": "Cuatro de Corazones", "value": 4, "priority": 3, "realValue": 4},
    "C05": {"literal": "Cinco de Corazones", "value": 5, "priority": 3, "realValue": 5},
    "C06": {"literal": "Seis de Corazones", "value": 6, "priority": 3, "realValue": 6},
    "C07": {"literal": "Siete de Corazones", "value": 7, "priority": 3, "realValue": 7},
    "C08": {"literal": "Ocho de Corazones", "value": 8, "priority": 3, "realValue": 0.5},
    "C09": {"literal": "Nueve de Corazones", "value": 9, "priority": 3, "realValue": 0.5},
    "C10": {"literal": "J de Corazones", "value": 10, "priority": 3, "realValue": 0.5},
    "C11": {"literal": "Q de Corazones", "value": 11, "priority": 3, "realValue": 0.5},
    "C12": {"literal": "K de Corazones", "value": 12, "priority": 3, "realValue": 0.5},

    "P01": {"literal": "As de Picas", "value": 1, "priority": 2, "realValue": 1},
    "P02": {"literal": "Dos de Picas", "value": 2, "priority": 2, "realValue": 2},
    "P03": {"literal": "Tres de Picas", "value": 3, "priority": 2, "realValue": 3},
    "P04": {"literal": "Cuatro de Picas", "value": 4, "priority": 2, "realValue": 4},
    "P05": {"literal": "Cinco de Picas", "value": 5, "priority": 2, "realValue": 5},
    "P06": {"literal": "Seis de Picas", "value": 6, "priority": 2, "realValue": 6},
    "P07": {"literal": "Siete de Picas", "value": 7, "priority": 2, "realValue": 7},
    "P08": {"literal": "Ocho de Picas", "value": 8, "priority": 2, "realValue": 0.5},
    "P09": {"literal": "Nueve de Picas", "value": 9, "priority": 2, "realValue": 0.5},
    "P10": {"literal": "J de Picas", "value": 10, "priority": 2, "realValue": 0.5},
    "P11": {"literal": "Q de Picas", "value": 11, "priority": 2, "realValue": 0.5},
    "P12": {"literal": "K de Picas", "value": 12, "priority": 2, "realValue": 0.5},

    "T01": {"literal": "As de Trevoles", "value": 1, "priority": 1, "realValue": 1},
    "T02": {"literal": "Dos de Trevoles", "value": 2, "priority": 1, "realValue": 2},
    "T03": {"literal": "Tres de Trevoles", "value": 3, "priority": 1, "realValue": 3},
    "T04": {"literal": "Cuatro de Trevoles", "value": 4, "priority": 1, "realValue": 4},
    "T05": {"literal": "Cinco de Trevoles", "value": 5, "priority": 1, "realValue": 5},
    "T06": {"literal": "Seis de Trevoles", "value": 6, "priority": 1, "realValue": 6},
    "T07": {"literal": "Siete de Trevoles", "value": 7, "priority": 1, "realValue": 7},
    "T08": {"literal": "Ocho de Trevoles", "value": 8, "priority": 1, "realValue": 0.5},
    "T09": {"literal": "Nueve de Trevoles", "value": 9, "priority": 1, "realValue": 0.5},
    "T10": {"literal": "J de Trevoles", "value": 10, "priority": 1, "realValue": 0.5},
    "T11": {"literal": "Q de Trevoles", "value": 11, "priority": 1, "realValue": 0.5},
    "T12": {"literal": "K de Trevoles", "value": 12, "priority": 1, "realValue": 0.5},
}

"""for id in cartas2:
    query = "INSERT INTO card (card_id, card_name, card_value, card_priority, card_real_value, deck_id) VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(query, (id, cartas2[id]["literal"], cartas2[id]["value"], cartas2[id]["priority"], cartas2[id]["realValue"], "POK"))
    db.commit()"""

"""query = "INSERT INTO deck (deck_id, deck_name) VALUES (%s,%s)"
cursor.execute(query, ("POK", "Poker"))
db.commit()"""

"""query = "DELETE  FROM card;"
cursor.execute(query)
db.commit()"""


players = {"11115555A":
               {"name": "Mario", "human": True, "bank": False, "initialCard": "", "priority": 1, "type": 40,
                "bet": 4, "points": 8, "cards": ["O12", "O11", "O10", "O07"], "roundPoints": 5},
           "22225555A":
               {"name": "Pedro", "human": True, "bank": True, "initialCard": "", "priority": 2, "type": 40,
                "bet": 4, "points": 8, "cards": ["C03", "B12"], "roundPoints": 5},
           "34343434H":
               {"name": "Bot1", "human": False, "bank": False, "initialCard": "", "priority": 3, "type": 30,
                "bet": 4, "points": 8, "cards": ["E10"], "roundPoints": 4},
           "11111111A":
               {"name": "Bot2", "human": False, "bank": False, "initialCard": "", "priority": 0, "type": 50,
                "bet": 4, "points": 0, "cards": [], "roundPoints": 0}
           }


cardgame = {'cardgame_id': '', 'players': '', 'start_hour': '', 'rounds': '', 'end_hour': ''}

player_game = {'cardgame_id': {'id_player_1': {'initial_card_id': 'card_id', 'starting_points': '', 'ending_points': ''}}}

player_game_round = {'round': {
    'id_player_1': {'is_bank': '', 'bet_points': '', 'starting_round_points': '', 'cards_value': '',
                    'endind_round_points': ''}}}

game = ["11115555A", "22225555A", "34343434H"]

cardgame_ids = []

letrasDni = ["T", "R", "W", "A", "G", "M", "Y", "F", "P", "D", "X", "B", "N",
             "J", "Z", "S", "Q", "V", "H", "L", "C", "K", "E"]

contextGame = {"maxRounds": 5}

