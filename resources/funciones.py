import datetime
import os
from resources.prints import *
from resources.bbdd_provisionales import *
import random
import math
import itertools

import mysql.connector

db = mysql.connector.connect(user="MAP", password="2023Proyecto",
                                   host="proyecto1.mysql.database.azure.com",
                                   database="seven_and_half",
                                   port="3306")
cursor = db.cursor()

def clear():
    # PRE: No le llega ningun parametro
    # POST: Limpia la pantalla de la cmd segun si el nombre del sistema es windows o no
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def order_list(llista, ordre="des"):
    # PRE: llista con valores no definidos. orde, por defecto "des", ordena de forma desdecendente cuando ordre = des,
    #      y ordena crecientemente cuando ordre = asc
    # POST: Devuelve el parametro llista ordenada segun el parametro ordre
    try:
        if type(llista) != list:
            raise ValueError("The parameter llista must to be a list")
        if ordre not in ["des", "asc"]:
            raise TypeError("The parameter ordre must to be des or asc")
        for i in range(1, len(llista) - 1):
            if type(llista[i]) != type(llista[i - 1]):
                raise TypeError("The list must to have the same variable type")

        # BUBBLE SORT
        for pasada in range(len(llista) - 1):
            lista_ordenada = True
            for i in range(len(llista) - 1 - pasada):

                if ordre == "des":
                    if llista[i] < llista[i + 1]:
                        lista_ordenada = False
                        aux = llista[i]
                        llista[i] = llista[i + 1]
                        llista[i + 1] = aux

                elif ordre == "asc":
                    if llista[i] > llista[i + 1]:
                        lista_ordenada = False
                        aux = llista[i]
                        llista[i] = llista[i + 1]
                        llista[i + 1] = aux

            if lista_ordenada:
                break

    except ValueError as e:
        print(e)
    except TypeError as e:
        print(e)
    return llista


def setGamePriority(mazo=[], jugadores=[]):
    # PRE: Introducimos la list(cartas) y la game=[]
    # Repartimos una carta a cada uno
    # Creamos otra lista en el mismo orden con los valores de las cartas para ordenarlas
    # POST: Devolvemos una lista de tuplas con (DNI, CARTA)
    mazo1 = mazo.copy()
    cartasRepartidas = {}
    cartasOrdenadas = []
    for i in range(len(jugadores)):
        cartaRandom = random.choice(mazo1)
        cartasRepartidas[jugadores[i]] = cartaRandom
        mazo1.remove(cartaRandom)
    mida_llista = len(jugadores)
    llista = []
    for i in cartasRepartidas:
        carta = cartasRepartidas[i]
        llista.append(cartas[carta]['value'])
    for i in range(mida_llista - 1):
        for j in range(0, mida_llista - i - 1):
            if llista[j] < llista[j + 1]:
                llista[j], llista[j + 1] = llista[j + 1], llista[j]
                jugadores[j], jugadores[j + 1] = jugadores[j + 1], jugadores[j]
            elif llista[j] == llista[j + 1] and cartas[cartasRepartidas[jugadores[j]]]['priority'] < \
                    cartas[cartasRepartidas[jugadores[j + 1]]]['priority']:
                jugadores[j], jugadores[j + 1] = jugadores[j + 1], jugadores[j]

    for i in jugadores:
        cartasOrdenadas.append((i, cartasRepartidas[i]))

    return cartasOrdenadas

def resetPoints():
    # PRE: No le llega ningun parametro
    # POST: Establece los puntos de los jugadores de la lista game a 20
    for i in game:
        players[i]['points'] = 20


def generate_game_id():
    # PRE: Pide la cantidad de ID que hay en la base de datos
    # POST: Suma 1 a ducha cantidad para que sea el nuevo ID
    query = "SELECT count(cardgame_id) FROM cardgame;"
    cursor.execute(query)
    result = cursor.fetchall()
    new_cardgame_id = result[0][0] + 1
    return new_cardgame_id


def fill_player_game(gameID, jugadores=[], card_id_list=[], starting_points_list=[], ending_points_list=[]):
    # PRE: Recibe la ID de la partida, la lista game, la lista de cartas, la lista de puntos iniciales y la lista
    # de puntos finales
    # POST: Devuelve el diccionario player_game con los datos estructurados
    player_game.update({gameID: ''})
    for i in range(len(jugadores)):
        if i == 0:
            player_game[gameID] = {jugadores[i]: {'initial_card_id': card_id_list[i], 'starting_points':
                starting_points_list[i], 'ending_points': ending_points_list[i]}}
        else:
            player_game[gameID][jugadores[i]] = {'initial_card_id': card_id_list[i], 'starting_points':
                starting_points_list[i], 'ending_points': ending_points_list[i]}
    return player_game

def fill_cardgame(gameID, num_players, start_hour = "", rounds = 0, end_hour = "", deck = ""):
    # PRE: gameID, ID de la partida; num_players, número de jugadores de la partida; start_hour, hora de comienzo;
    #      end_hour, hora al finalizar la partida; deck, mazo usado en la partida
    # POST: guarda los datos de la partida en el diccionario cardgame
    cardgame[gameID] = {'players': num_players, "start_hour": start_hour, 'rounds': rounds, 'end_hour': end_hour, "deck": deck}

def playergameround(gameID, round, jugadores = [], start_points = [], end_points = [], id_bank = ""):
    for i in range(len(jugadores)):
        if jugadores[i] == id_bank:
            stats = {'is_bank': True, 'bet_points': None, 'starting_round_points': start_points[i],
                    'cards_value': players[jugadores[i]]["roundPoints"], 'ending_round_points': end_points[i]}
        else:
            stats = {'is_bank': False, 'bet_points': players[jugadores[i]]["bet"], 'starting_round_points': start_points[i],
                     'cards_value': players[jugadores[i]]["roundPoints"], 'ending_round_points': end_points[i]}

        player_game_round[gameID][round][jugadores[i]] = stats


def checkMinimun2PlayerWithPoints():
    # Funcion que devuelve True si hay 2 o más jugadores con puntos, de lo contrario devuelve False

    contador = 0
    for i in game:
        if players[i]['points'] > 0:
            contador += 1

    if contador < 2:
        seguir_jugando = False
    else:
        seguir_jugando = True

    return seguir_jugando

def orderAllPlayers():
    # Funcion que crea una lista con los puntos de los jugadores y ordena la lista de jugadores de forma inversa segun su prioridad, pone la banca al principio
    # POST: Devuelve una lista con los ID_player ordenados.
    prioridad = []
    for i in game:
        prioridad.append(players[i]['priority'])

    mida_llista = len(prioridad)

    for i in range(mida_llista - 1):
        for j in range(0, mida_llista - i - 1):
            if prioridad[j] < prioridad[j + 1]:
                prioridad[j], prioridad[j + 1] = prioridad[j + 1], prioridad[j]
                game[j], game[j + 1] = game[j + 1], game[j]

    for i in game:
        if players[i]['bank']:
            game.remove(i)
            game.append(i)

    return game

def setBets():
    # Funcion que establece las apuestas según el tipo de jugador
    for i in game:
        if players[i]['bank'] is True:
            players[i]['bet'] = 0
        elif players[i]['points'] > 0:
            players[i]['bet'] = math.ceil(players[i]['points'] / 100 * players[i]['type'])



def standardRound(id, mazo1, tirada_cartas = []):

    while True:
        if players[id]['bank'] == False:

            if players[id]['roundPoints'] == 0:
                nueva_carta = random.choice(mazo1)
                mazo1.remove(nueva_carta)
                tirada_cartas.append(nueva_carta)
                players[id]['roundPoints'] += cartas[nueva_carta]['realValue']
            else:
                if chanceExceedingSevenAndHalf(id, mazo1) <= players[id]['type']:
                    nueva_carta = random.choice(mazo1)
                    mazo1.remove(nueva_carta)
                    tirada_cartas.append(nueva_carta)
                    players[id]['roundPoints'] += cartas[nueva_carta]['realValue']

                else:
                    return tirada_cartas
        else:
            tirar = 0
            if baknOrderNewCard(id) or chanceExceedingSevenAndHalf(id, mazo1) <= players[id]['type']:
                if players[id]['roundPoints'] == 0:
                    nueva_carta = random.choice(mazo1)
                    mazo1.remove(nueva_carta)
                    tirada_cartas.append(nueva_carta)
                    players[id]['roundPoints'] += cartas[nueva_carta]['realValue']

                else:
                    for i in game:
                        if players[i]['bank'] is False:
                            if 7.5 >= players[i]['roundPoints'] > players[id]['roundPoints']:
                                tirar += 1
                    if tirar > 0:
                        nueva_carta = random.choice(mazo1)
                        mazo1.remove(nueva_carta)
                        tirada_cartas.append(nueva_carta)
                        players[id]['roundPoints'] += cartas[nueva_carta]['realValue']
                    else:
                        return tirada_cartas

            else:
                return tirada_cartas


def getOpt(textOpts="", inputOptText="", rangeList=[], exceptions=[]):
    # PRE: Al parámetro textOpts se le pasa el string con las opciones del menú
    #      Al parámetro inputOpt se le pasa el string con la frase que pide que escojamos una opción
    #      El parámetro RangeList contiene las opciones contempladas por el menu
    #      El parámetro exceptions contiene las posibles excepciones que pueden generarse
    # POST: Devolverá un valor de RangeList si la selección es correcta y devolverá un valor de exceptions si ha ocurrido
    #       un error
    correct = False
    opc = ''
    input_text = ''.ljust(50) + inputOptText
    while not correct:
        clear()
        print(textOpts)
        opc = input(input_text)
        if opc in exceptions:
            correct = True
        else:
            try:
                opc = int(opc)
                if opc not in rangeList and opc not in exceptions:
                    raise TypeError(incorrectopt)
                else:
                    correct = True
            except ValueError:
                print(onlynumbers)
                input(enter)
            except TypeError as e:
                print(e)
                input(enter)
    return opc


def func_text_opts(text='', header=''):
    if header == '':
        seq = '\n'
    else:
        seq = header + '\n\n'
    optlist = text.split(',')
    for i in optlist:
        seq += ''.ljust(50) + i + '\n'
    return seq


def orderPlayersByPoints(listaDNIs):
    dic_PL_Points = {}
    # Llamamos a una funcion que pida los DNI y calcule los puntos que tiene un jugador a la BBDD,
    # y los devuelva en formato diccionario; dni: puntos

    for pasada in range(listaDNIs - 1):
        lista_ordenada = True
        for i in range(len(listaDNIs) - 1 - pasada):
            if dic_PL_Points[listaDNIs[i]] < dic_PL_Points[listaDNIs[i + 1]]:
                lista_ordenada = False
                aux = listaDNIs[i]
                listaDNIs[i] = listaDNIs[i + 1]
                listaDNIs[i + 1] = aux
        if lista_ordenada:
            break
    return listaDNIs


def chanceExceedingSevenAndHalf(id, mazo2):
    bad_cards = 0
    for i in mazo2:
        if cartas[i]["realValue"] + players[id]["roundPoints"] > 7.5:
            bad_cards += 1

    return (bad_cards * 100) / len(mazo2)


def printPlayerStats(id):
    clear()
    print('*'*140 + '\n' + gameprint)
    print(" Stats of {} ".format(players[id]["name"]).center(140, "*"))
    for i in players[id]:
        if i == "cards":
            print(str(i).ljust(55), end="")
            primero = True
            for j in players[id]["cards"]:
                if primero:
                    primero = False
                    print(str(j), sep="", end="")
                else:
                    print(";", str(j), sep="", end="")
            print()
        else:
            print(str(i).ljust(55), str(players[id][i]).ljust(4), sep="")


def baknOrderNewCard(id):
    earnings = 0
    looses = 0
    ret = False
    for i in game:
        if i != id:
            if (players[i]["roundPoints"] <= 7.5 and players[i]["roundPoints"] <= players[id]["roundPoints"]) or \
                    players[i]["roundPoints"] > 7.5:
                earnings += players[i]["bet"]
            else:
                if players[i]["roundPoints"] == 7.5:
                    looses += players[i]["bet"] * 2
                else:
                    looses += players[i]["bet"]
    if looses - earnings >= players[id]['points']:
        ret = True

    return ret


def nif_validator():
    # PRE:
    # POST: Devuelve un NIF válido
    getPlayers()
    correct = False
    newnif = ''
    while not correct:
        try:
            newnif = input('Introduce the NIF: ')
            if not len(newnif) == 9:
                raise ValueError('Invalid NIF length')
            elif not newnif[:8].isdigit():
                raise ValueError('Invalid NIF numbers')
            elif not newnif[8].isalpha():
                raise ValueError('Invalid NIF letter')
            elif not letrasDni[int(newnif[:8]) % 23].casefold() == newnif[8].casefold():
                raise ValueError('Incorrect NIF letter')
            elif newnif.upper() in players:
                raise ValueError('That NIF already exists in the database')
            correct = True
        except ValueError as e:
            print(e)

    return newnif.upper()

def savePlayer(tup_player):
    query = "INSERT INTO player (player_id, player_name, player_risk, human) VALUES (%s,%s,%s,%s);"
    cursor.execute(query, tup_player)
    db.commit()

def getPlayers():
    players.clear()
    query = "SELECT * FROM player;"
    cursor.execute(query)
    result = cursor.fetchall()
    for i in result:
        dict_aux = {}
        dni = i[0]
        name = i[1]
        profile = i[2]
        if i[3] == 1:
            human = True
        else:
            human = False
        tup = newPlayer(dni, name, profile, human)
        dict_aux = {tup[0]: tup[1]}
        players.update(dict_aux)

def delBBDDPlayer(nif):
    query = "DELETE FROM player WHERE player_id = '" + nif + "';"
    cursor.execute(query)
    db.commit()

def removeBBDDPlayer():
    while True:
        clear()
        getPlayers()
        showhPlayersBBDD()
        opt = input("Option (-id to remove player, -1 to go back): ")
        try:
            if len(opt) < 2:
                raise TypeError()
            elif opt[0] == "-":
                if opt[1] == "1" and len(opt) == 2:
                    clear()
                    break
                elif len(opt) == 10 and opt[1:] in list(players.keys()) and opt[1:] not in game:
                    print(''.ljust(50) + opt[1:], 'has been deleted')
                    input()
                    delBBDDPlayer(opt[1:])
                elif opt[1:] in game:
                    print(''.ljust(50)+"You can't remove a player if it's in game")
                else:
                    raise TypeError()
            else:
                raise TypeError()
        except TypeError:
            print("Invalid Option".center(140, "="))
            print(" " * 40, "Enter to continue".center(60), sep="")
            input("")

def showhPlayersBBDD():
    bots = []
    humans = []
    for id in players:
        if players[id]["human"]:
            humans.append(id)
        else:
            bots.append(id)
    if len(humans) > 0:
        order_list(humans, "asc")
    if len(bots) > 0:
        order_list(bots, "asc")
    print("Select Players".center(140, "*"))
    print("Bot Players".center(69), "||", "Human Players".center(69), "\n", "-"*140,  sep="")
    print("ID".ljust(11), " "*9, "Name".ljust(18), " "*5, "Type".ljust(26), "||", "ID".ljust(11), " "*9, "Name".ljust(15), " "*5, "Type".ljust(26), sep="")
    print("*"*140)

    while len(bots) > 0 or len(humans) > 0:
        string = ""
        if len(bots) > 0:
            string = bots[0].ljust(11) + " "*9 + players[bots[0]]["name"].ljust(18) + " "*5
            if players[bots[0]]["type"] == 30:
                string += "Cautious".ljust(26)
            elif players[bots[0]]["type"] == 40:
                string += "Moderated".ljust(26)
            elif players[bots[0]]["type"] == 50:
                string += "Bold".ljust(26)
            bots.remove(bots[0])
        else:
            string = " "*69
        string += "||"
        if len(humans) > 0:
            string += humans[0].ljust(11) + " " * 9 + players[humans[0]]["name"].ljust(15) + " " * 5
            if players[humans[0]]["type"] == 30:
                string += "Cautious".ljust(26)
            elif players[humans[0]]["type"] == 40:
                string += "Moderated".ljust(26)
            elif players[humans[0]]["type"] == 50:
                string += "Bold".ljust(26)
            humans.remove(humans[0])
        print(string)
    print("*"*140)

def addRemovePlayers():
    while True:
        opt = getOpt(func_text_opts(add_remove_text, bbddplayers), opt_text, [1, 2, 3, 4])
        if opt == 1:
            tup_player = setNewPlayer()
            savePlayer(tup_player)
        elif opt == 2:
            tup_player = setNewPlayer(human = False)
            savePlayer(tup_player)
        elif opt == 3:
            removeBBDDPlayer()
        elif opt == 4:
            return False


def setMaxRounds():
    correct = False
    rounds = 5
    while not correct:
        clear()
        print(setmaxrounds)
        rounds = input(''.ljust(50)+"Max Rounds: ")
        if not rounds.isdigit():
            print(''.ljust(50)+"Please, only introduce numbers")
            input(''.ljust(50)+'Enter to continue')
        elif int(rounds) <= 0 or int(rounds) > 30:
            print(''.ljust(50)+"Please, introduce a number bigger than 0 and smaller than 30")
            input(''.ljust(50)+'Enter to continue')
        else:
            correct = True

            print(''.ljust(50)+'Established maximum of rounds to', rounds)
            input(''.ljust(50)+'Enter to continue')
    contextGame["maxRounds"] = int(rounds)


def tipo_de_riesgo(id):
    riesgo = ''
    if players[id]['type'] == 30:
        riesgo = 'Cautious'
    elif players[id]['type'] == 40:
        riesgo = 'Moderated'
    elif players[id]['type'] == 50:
        riesgo = 'Bold'

    return riesgo

def bot_or_human(dni):
    if players[dni]['human'] is True:
        return 'Human'
    elif players[dni]['human'] is False:
        return 'Bot'

def setPlayersGame():
    getPlayers()
    clear()
    actualPlayers = setgameplayers + '\n' * 3 + '********************** Actual Players In Game **********************'.center(
        140) + '\n'

    textinput = 'Option (id to add to game, -id to remove player, sh to show actual players in game, -1 to go back):\n'
    jugadores_not_in_game = list(players)
    for i in game:
        if i in jugadores_not_in_game:
            jugadores_not_in_game.remove(i)
    if len(game) == 0:
        actualPlayers += 'There is no players in game'.center(140)
    else:
        for i in game:
            centrar_texto = str(i).ljust(12) + '  ' + players[i]['name'].ljust(30) + '  ' + bot_or_human(i).ljust(8) + \
                            '  ' + tipo_de_riesgo(i).ljust(12)
            actualPlayers += centrar_texto.center(140) + '\n'
    print(actualPlayers)
    input(enter)

    while True:
        clear()
        actualPlayers = '\n' * 3 + '********************** Actual Players In Game **********************'.center(140) + '\n'
        bots = []
        humans = []
        for i in jugadores_not_in_game:
            if players[i]['human'] is True:
                humans.append(i)
            else:
                bots.append(i)
        tabla_jugadores = set_game_players_cabecera

        for humanos, boots in itertools.zip_longest(humans, bots, fillvalue=None):
            if boots is None:
                tabla_jugadores += ''.ljust(14) + '  ' + \
                                   ''.ljust(30) + '  ' + ''.ljust(20) + ' ' + '||' + '  ' + humanos.ljust(14) + '  ' + \
                                   players[humanos]['name'].ljust(30) + '  ' + tipo_de_riesgo(humanos).ljust(
                    18) + ' ' + '\n'
            elif humanos is None:
                tabla_jugadores += boots.ljust(14) + '  ' + \
                                   players[boots]['name'].ljust(30) + '  ' + tipo_de_riesgo(boots).ljust(20) \
                                   + ' ' + '||' + '  ' + ''.ljust(14) + '  ' + ''.ljust(30) + '  ' + ''.ljust(
                    18) + ' ' + '\n'
            else:
                tabla_jugadores += boots.ljust(14) + '  ' + \
                                   players[boots]['name'].ljust(30) + '  ' + tipo_de_riesgo(boots).ljust(20) \
                                   + ' ' + '||' + '  ' + humanos.ljust(14) + '  ' + \
                                   players[humanos]['name'].ljust(30) + '  ' + tipo_de_riesgo(humanos).ljust(
                    18) + ' ' + '\n'
        tabla_jugadores += '*' * 140

        print(tabla_jugadores)
        nuevo_jugador = input(textinput)
        if len(nuevo_jugador) == 0:
            print(invalidoption)
            input(enter)
        else:
            if nuevo_jugador.upper() in jugadores_not_in_game:
                if len(game) == 6:
                    print('\n'+'Maxim number of players in game reached!!'.center(140)+'\n')
                else:
                    game.append(nuevo_jugador.upper())
                    jugadores_not_in_game.remove(nuevo_jugador.upper())

            elif nuevo_jugador[0] == '-' and nuevo_jugador[1:].upper() in game:
                game.remove(nuevo_jugador[1:].upper())
                jugadores_not_in_game.append(nuevo_jugador[1:].upper())
            elif nuevo_jugador == 'sh':
                pass
            else:
                try:
                    if int(nuevo_jugador) == -1:
                        break
                    else:
                        print(invalidoption)
                        input(enter)
                        continue
                except ValueError:
                    print(invalidoption)
                    input(enter)
                    continue
            if len(game) == 0:
                actualPlayers += 'There is no players in game'.center(140)
            else:
                for i in game:
                    centrar_texto = str(i).ljust(12) + '  ' + players[i]['name'].ljust(30) + '  ' + bot_or_human(
                        i).ljust(8) + '  ' + tipo_de_riesgo(i).ljust(12)
                    actualPlayers += centrar_texto.center(140) + '\n'
            print(actualPlayers)
            input(enter)


def newRandomDNI():
    # PRE: No recibe ningun parametro
    # POST: Actualiza y descarga la lista de jugadores de la base de datos y genera un ID aleatorio que no este
    # en dicha lista. Devuelve el ID generado
    getPlayers()
    correct = True
    DNI = ''
    while correct:
        DNI = random.randint(10000000, 99999999)
        letra = letrasDni[DNI % 23]
        DNI = str(DNI) + letra.upper()
        if DNI not in list(players):
            correct = False

    return DNI

def setNewPlayer(human=True):
    # PRE: Human=True
    # POST: Te pide que introduzcas DNI, el perfil de riesgo y el nombre, devuelve una tupla con ID del jugador,
    # nombre, perfil de riesgo y human = true
    dni = ""
    profile = 0
    name = ""
    if human:
        opt = getOpt(func_text_opts("1)Random DNI,2)Custom DNI"), "Option: ", [1, 2])
        if opt == 1:
            dni = newRandomDNI()
        else:
            dni = nif_validator()
    else:
        dni = newRandomDNI()

    opt = getOpt(func_text_opts("Select your Profile:,1)Cautious,2)Moderated,3)Bold"), "Option: ", [1, 2, 3])
    if opt == 1:
        profile = 30
    elif opt == 2:
        profile = 40
    else:
        profile = 50

    correct = False
    while not correct:
        name = input(''.ljust(50)+"Name: ")
        if not name.isalnum():
            print(''.ljust(50)+"Incorrect name, please, enter a name not empty with only letters")
        else:
            correct = True
    tup_player = (dni, name, profile, human)
    return tup_player


def newPlayer(dni, name, profile, human):
    # PRE: ID del jugador, nombre, riesgo, human (True or False)
    # POST: Devuelve una tupla con el ID del jugador y el diccionario con los datos del nuevo jugador
    dic_aux = {"name": name, "human": human, "bank": False, "initialCard": "", "priority": 0, "type": profile,
               "bet": 4, "points": 0, "cards": [], "roundPoints": 0}
    return (dni, dic_aux)


def printStats(titulo_superior="", titulo_inferior=''):
    # PRE: titulo_superior recibe una string con la parte superior de la cabecera, titulo_inferior recibe una string
    # con la parte inferior de la cabecera
    # POST: Imprime los Stats de la partida
    clear()

    print(titulo_superior.center(140, "*"))
    print(gameprint)
    print(titulo_inferior.center(140, "*"))
    lista = ["Name", "Human", "Priority", "Type", "Bank", "Bet", "Points", "Cards", "Roundpoints"]
    arguments = ["name", "human", "priority", "type", "bank", "bet", "points", "cards", "roundPoints"]
    for i in range(0, 9):
        seq = lista[i].ljust(20) + " "*5
        for j in game[:3]:
            if arguments[i] != "cards":
                seq += str(players[j][arguments[i]]).ljust(40)
            else:
                cards = ""
                primero = True
                for k in players[j]["cards"]:
                    if primero:
                        primero = False
                        cards += k
                    else:
                        cards += ";" + k
                seq += cards.ljust(40)
        print(seq)
    if len(game) > 3:
        print('*'*140)
        for i in range(0, 9):
            seq = lista[i].ljust(20) + " " * 5
            for j in game[3:]:
                if arguments[i] != "cards":
                    seq += str(players[j][arguments[i]]).ljust(40)
                else:
                    cards = ""
                    primero = True
                    for k in players[j]["cards"]:
                        if primero:
                            primero = False
                            cards += k
                        else:
                            cards += ";" + k
                    seq += cards.ljust(40)
            print(seq)
def set_card_deck():
    # PRE: No recibe ningun parametro
    # POST: Pide una ID de un mazo por consola y descarga el mazo de la base de datos al diccionario cartas
    query = "select deck_id from deck;"
    cursor.execute(query)
    result = cursor.fetchall()
    id_deck = []
    seq = ""
    primero = True
    for id in result:
        if primero:
            primero = False
            id_deck.append(id[0])
            seq += id[0]
        else:
            id_deck.append(id[0])
            seq += "," + id[0]

    opt = getOpt(func_text_opts(seq, deckofcards), 'Option(-1 to go back): ', [-1], id_deck)
    print(''.ljust(50) + 'The deck {} has been chosen.'.format(opt))
    if opt == -1:
        print(''.ljust(50) + 'Deck not chosen.')
        input(enter)
    else:
        query = "select * from card where deck_id = %s;"
        cursor.execute(query, (opt,))
        result = cursor.fetchall()
        contextGame['deck'] = opt

        for row in result:
            dict_aux = {"literal": row[1], "value": row[2], "priority": row[3], "realValue": row[4]}
            cartas[row[0]] = dict_aux
        input(enter)

def distributionPointAndNewBankCandidates(banco, sorted_players_main=[]):
    # PRE: ID del jugador que es el banco, lista de jugadores ordenados inversamente por prioridad ([4,3,2,1])
    # POST: Hace los calculos del resultado de la ronda.
    # Los puntos que pierden los jugadores se les resta inmediatamente, los que ganan se les suma en funcion de la
    # prioridad, la banca hace una resta entre los puntos ganados y perdidos y se suma o resta el resultado.
    # Establecemos la nueva banca y eliminamos los jugadores sin puntos.

    candidatos_banca = []
    nueva_banca = False
    banca_debe = 0
    banca_cobra = 0
    sieteymedio = []

    sorted_players = sorted_players_main.copy()
    sorted_players.reverse()
    sorted_players.remove(banco)
    jugadores_para_cobrar = []
    if players[banco]['roundPoints'] == 7.5:
        for j in sorted_players:
            banca_cobra += players[j]['bet']
            players[j]['points'] -= players[j]['bet']


    elif players[banco]['roundPoints'] < 7.5:
        for j in sorted_players:
            if players[banco]['roundPoints'] < players[j]['roundPoints'] < 7.5:
                banca_debe += players[j]['bet']
                jugadores_para_cobrar.append(j)
            elif players[banco]['roundPoints'] > players[j]['roundPoints']:
                banca_cobra += players[j]['bet']
                players[j]['points'] -= players[j]['bet']
            elif players[banco]['roundPoints'] == players[j]['roundPoints']:
                banca_cobra += players[j]['bet']
                players[j]['points'] -= players[j]['bet']
            elif players[j]['roundPoints'] > 7.5:
                banca_cobra += players[j]['bet']
                players[j]['points'] -= players[j]['bet']
            elif players[j]['roundPoints'] == 7.5:
                banca_debe += players[j]['bet'] * 2
                jugadores_para_cobrar.append(j)
                jugadores_para_cobrar.append(j)
                candidatos_banca.append(j)
                nueva_banca = True



    elif players[banco]['roundPoints'] > 7.5:
        for j in sorted_players:
            if players[j]['roundPoints'] < 7.5:
                banca_debe += players[j]['bet']
                jugadores_para_cobrar.append(j)
            elif players[j]['roundPoints'] == 7.5:
                banca_debe += players[j]['bet'] * 2
                candidatos_banca.append(j)
                jugadores_para_cobrar.append(j)
                jugadores_para_cobrar.append(j)
                nueva_banca = True


    dinero_restante = players[banco]['points'] + banca_cobra

    if dinero_restante < banca_debe:
        for i in jugadores_para_cobrar:
            if dinero_restante >= players[i]['bet']:
                players[i]['points'] += players[i]['bet']
                dinero_restante -= players[i]['bet']
            else:
                players[i]['points'] += dinero_restante
                dinero_restante = 0

        players[banco]['points'] = 0
        players[banco]['bank'] = False
        nueva_banca = True


    else:
        players[banco]['points'] += banca_cobra - banca_debe
        if len(jugadores_para_cobrar) > 0:
            for i in jugadores_para_cobrar:
                players[i]['points'] += players[i]['bet']

    for indice in range(len(game) -1, -1, -1):
        if players[game[indice]]['points'] < 1:
            game.remove(game[indice])

    if nueva_banca:
        players[banco]['bank'] = False
        lista_ordenada = orderAllPlayers().copy()
        for i in lista_ordenada:
            if i not in candidatos_banca:
                lista_ordenada.remove(i)
        if len(lista_ordenada) > 0:
            for i in lista_ordenada:
                if players[i]['roundPoints'] == 7.5:
                    sieteymedio.insert(0, i)
            if len(sieteymedio) > 0:
                players[sieteymedio[0]]['bank'] = True
            else:
                players[lista_ordenada[-1]]['bank'] = True
        else:
            players[orderAllPlayers()[-1]]['bank'] = True



def settings():
    # PRE: No recibe ningun parametro
    # POST: Devuelve el menu settings: Set Players game, set card deck y set max rounds.
    # Devulve False si se selecciona 4
    while True:
        option = getOpt(func_text_opts(opts_settings, settings_print), opt_text, list(range(1, 5)))
        if option == 1:
            setPlayersGame()
        elif option == 2:
            set_card_deck()
        elif option == 3:
            setMaxRounds()
        elif option == 4:
            return False

def reset_stats():
    # PRE: No recibe ningun parametro
    # POST: Establece los roundPoints y la lista de cartas a 0 y a lista vacía.
    for i in game:
        players[i]['roundPoints'] = 0
        players[i]['cards'] = []

def reset_bets():
    # PRE: No recibe ningun parametro
    # POST: Establece las bets de los jugadores a 0
    for i in game:
        players[i]['bet'] = 0

def winner():
    # PRE: Recoge los jugadores restantes al final de la partida y sus puntos.
    # POST: Devuelve el ganador segun los puntos restantes.
    game1 = game.copy()
    puntos = []
    for i in game:
        puntos.append(players[i]['points'])

    mida_llista = len(puntos)

    for i in range(mida_llista - 1):
        for j in range(0, mida_llista - i - 1):
            if puntos[j] < puntos[j + 1]:
                puntos[j], puntos[j + 1] = puntos[j + 1], puntos[j]
                game1[j], game1[j + 1] = game1[j + 1], game1[j]
    return game1[0]

def turn_of_human(ronda, player_id, numero_ronda, mazo1):
    tirada_cartas = []
    carta_pedida = False
    while True:
        option = getOpt(func_text_opts(human_opts, ronda), opt_text, list(range(1, 7)))
        if option == 1:
            printPlayerStats(player_id)
            input(enter)
        elif option == 2:
            printStats(titulo_inferior=' Round {}, Turn of {} '.format(numero_ronda, players[player_id]['name']))
            input(enter)

        elif option == 3:
            if players[player_id]['bank'] is True:
                print(''.ljust(50) + "You are the bank, therefore you can't bet.")
                input(ljust_enter)
            elif carta_pedida:
                print(''.ljust(50) + "Can't change the bet if you have already ordered a card.")
                input(ljust_enter)
            else:
                new_bet = 0
                correct = False
                clear()
                while not correct:
                    try:
                        new_bet = int(input(''.ljust(50) + 'Set new Bet: '))
                        if new_bet > players[player_id]['points'] or new_bet < 1:
                            raise TypeError(''.ljust(50)+'The new bet has to be between 1 and {}'.format(players[player_id]['points']))
                        else:
                            correct = True
                    except ValueError:
                        print(''.ljust(50)+'Please, introduce only numbers')

                    except TypeError as e:
                        print(e)
                players[player_id]['bet'] = new_bet
                input(enter)

        elif option == 4:
            print(''.ljust(50) + 'Order Card')
            carta_pedida = True
            if len(tirada_cartas) == 0:
                nueva_carta = random.choice(mazo1)
                mazo1.remove(nueva_carta)
                tirada_cartas.append(nueva_carta)
                players[player_id]['roundPoints'] += cartas[nueva_carta]['realValue']
                print(''.ljust(50) + 'The new card is {}'.format(cartas[nueva_carta]['literal']))
                print(''.ljust(50) + 'Now you have {} points'.format(players[player_id]['roundPoints']))
                input(ljust_enter)
            else:
                if players[player_id]['roundPoints'] >= 7.5:
                    print(''.ljust(50) + "You have 7.5 points or more! You're not allowed to order another card.")
                else:
                    print(''.ljust(50) + 'Chance of exceeding 7.5 = {:.2f}%'.format(chanceExceedingSevenAndHalf(player_id, mazo1)))
                    sure = input(''.ljust(50) + 'Are you sure you want to order a new card? Y/y = Yes, another key = Not: ')
                    if sure.casefold() == 'y':
                        nueva_carta = random.choice(mazo1)
                        mazo1.remove(nueva_carta)
                        tirada_cartas.append(nueva_carta)
                        players[player_id]['roundPoints'] += cartas[nueva_carta]['realValue']
                        print(''.ljust(50) + 'The new card is {}'.format(cartas[nueva_carta]['literal']))
                        print(''.ljust(50) + 'Now you have {} points'.format(players[player_id]['roundPoints']))

                    else:
                        print(''.ljust(50) + 'Card not ordered')

                input(ljust_enter)
            players[player_id]['cards'] = tirada_cartas
        elif option == 5:
            players[player_id]['cards'] = (standardRound(player_id, mazo1, tirada_cartas))
            printStats(titulo_inferior=' Round {}, Turn of {} '.format(numero_ronda, players[player_id]['name']))
            input(enter)
            break
        elif option == 6:
            printStats(titulo_inferior=' Round {}, Turn of {} '.format(numero_ronda, players[player_id]['name']))
            input(enter)
            break

def play_game():
    getPlayers()
    ini_hour = datetime.datetime.now()
    send = True
    resetPoints()
    banca_debe = 0
    banca = ''
    order = setGamePriority(list(cartas), game)
    jugadores_ordenados = []
    ply_perma = []
    ini_cards = []
    for tup in order:
        ply_perma.append(tup[0])
        ini_cards.append(tup[1])
    priority = 0
    gameID = generate_game_id()
    player_game_round[gameID] = {}
    for i in order:
        jugadores_ordenados.append(i[0])
        priority += 1
        players[i[0]]['priority'] = priority
        players[i[0]]['initialCard'] = i[1]
        if priority == 1:
            banca = i[0]
            players[i[0]]['bank'] = True
    rounds = 0
    for i in range(0, contextGame['maxRounds']):
        mazo = list(cartas)
        rounds += 1
        reset_stats()
        setBets()
        if i == 0:
            printStats(titulo_superior=' ROUND 1 ')
            input(enter)
        jugadores_ordenados = orderAllPlayers()
        # ORDENAR JUGADORES EN JUGADORES_ORDENADOS CADA RONDA
        start_pts = []
        for id in jugadores_ordenados:
            start_pts.append(players[id]["points"])
        # GUARDAMOS LOS PUNTOS INICIALES

        for jugador in jugadores_ordenados:
            if players[jugador]['human'] is True:
                imprimir_ronda = '*'*140 + '\n' + gameprint + ' Round {}, Turn of {} '.format(i+1, players[jugador]['name']).center(140, '*')
                turn_of_human(imprimir_ronda, jugador, rounds, mazo)
            else:
                players[jugador]['cards'] = (standardRound(jugador, mazo, []))
                printStats(titulo_inferior=' Round {}, Turn of {} '.format(i+1, players[jugador]['name']))
                input(enter)
        distributionPointAndNewBankCandidates(banca, jugadores_ordenados)

        end_pts_round = []
        for id in jugadores_ordenados:
            end_pts_round.append(players[id]["points"])
        # GUARDAMOS LOS PUNTOS FINALES
        player_game_round[gameID][rounds] = {}
        playergameround(gameID, rounds, jugadores_ordenados, start_pts, end_pts_round, banca)

        reset_bets()
        for j in game:
            if players[j]['bank'] is True:
                banca = j
        printStats(titulo_superior=' STATS AFTER ROUND {} '.format(i+1))

        if not checkMinimun2PlayerWithPoints():
            break
        out = input('Enter to continue to new Round, exit to leave the game: ')

        if out == 'exit':
            send = False
            break
    str_pts = []
    end_pts = []

    for id in ply_perma:
        str_pts.append(20)
        if players[id]["points"] < 20:
            end_pts.append(players[id]["points"] - 20)
        else:
            end_pts.append(players[id]["points"])
    end_hour = datetime.datetime.now()
    fill_player_game(gameID, ply_perma, ini_cards, str_pts, end_pts)
    fill_cardgame(gameID, len(ply_perma), str(ini_hour), rounds, str(end_hour), contextGame["deck"])

    print(gameover)
    print('The winner is {} - {}, in {} rounds, with {} points.'.format(winner(), players[winner()]['name'], rounds,
                                                                        players[winner()]['points']).center(140))
    if send:
        query = "INSERT INTO cardgame (cardgame_id, players, rounds, start_hour, end_hour, deck_id) " \
                "VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (gameID, cardgame[gameID]["players"], cardgame[gameID]["rounds"], cardgame[gameID]["start_hour"],
                               cardgame[gameID]["end_hour"], cardgame[gameID]["deck"]))
        db.commit()
        for id in player_game[gameID]:
            query = "INSERT INTO player_game (cardgame_id, player_id, initial_card_id, starting_points, ending_points)" \
                    "VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(query, (gameID, id, player_game[gameID][id]["initial_card_id"], player_game[gameID][id]["starting_points"],
                                   player_game[gameID][id]["ending_points"]))
            db.commit()

        for round in player_game_round[gameID]:
            for id in player_game_round[gameID][round]:
                query = "INSERT INTO player_game_round (cardgame_id, round_num, player_id, bet_points, is_bank, cards_value," \
                        "starting_round_points, ending_round_points) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(query, (gameID, round, id, player_game_round[gameID][round][id]["bet_points"],
                                       player_game_round[gameID][round][id]["is_bank"],
                                       player_game_round[gameID][round][id]["cards_value"],
                                       player_game_round[gameID][round][id]["starting_round_points"],
                                       player_game_round[gameID][round][id]["ending_round_points"]))
                db.commit()

    input(enter)
    game.clear()



def reports():
    while True:
        seq = "1)Number of players who have been bank in each game,2)Average bet in each game," \
              "3)Average bet in the first round in each game,4)Average bet in the last round in each game," \
              "5)Player who places the lowest bet per game,6)List of games won by Bots," \
              "7)Player who places the highest bet in each game"
        opt = getOpt(func_text_opts(seq, reports_header), "Option(0 to go back): ", [0, 1, 2, 3, 4, 5, 6, 7])
        if opt == 1:
            clear()
            print(reports_header)
            print("Number of players who have been bank in each game".center(140))
            query = "select pb.cardgame_id, count(pb.player_id) from (select player_id, cardgame_id from player_game_round where is_bank = 1 group by player_id, cardgame_id) as pb group by cardgame_id;"
            cursor.execute(query)
            result = cursor.fetchall()
            print(" ".ljust(50), "Game ID".ljust(14), "Number of Banks", sep="")
            for row in result:
                print(" ".ljust(50), str(row[0]).ljust(14), row[1], sep="")
            input(ljust_enter)
        elif opt == 2:
            clear()
            print(reports_header)
            print("Average bet in each game".center(140))
            query = "select pb.cardgame_id, avg(pb.bet_points) from (select cardgame_id, bet_points from player_game_round) as pb group by pb.cardgame_id;"
            cursor.execute(query)
            result = cursor.fetchall()
            print(" ".ljust(50), "Game ID".ljust(14), "Average bet", sep="")
            for row in result:
                print(" ".ljust(50), str(row[0]).ljust(14), row[1], sep="")
            input(ljust_enter)
        elif opt == 3:
            clear()
            print(reports_header)
            print("Average bet in the first round in each game".center(140))
            query = "select ab.cardgame_id, avg(ab.bet_points) from (select cardgame_id, bet_points from player_game_round where round_num = 1 and bet_points is not NULL) as ab group by ab.cardgame_id;"
            cursor.execute(query)
            result = cursor.fetchall()
            print(" ".ljust(50), "Game ID".ljust(14), "Average bet", sep="")
            for row in result:
                print(" ".ljust(50), str(row[0]).ljust(14), row[1], sep="")
            input(ljust_enter)
        elif opt == 4:
            clear()
            print(reports_header)
            print("Average bet in the last round in each game".center(140))
            query = "select p.cardgame_id, avg(p.bet_points) from (select cardgame_id, max(round_num) as last_round from player_game_round group by cardgame_id) as ab, player_game_round p  where p.cardgame_id = ab.cardgame_id and round_num = ab.last_round group by p.cardgame_id;"
            cursor.execute(query)
            result = cursor.fetchall()
            print(" ".ljust(50), "Game ID".ljust(14), "Average bet", sep="")
            for row in result:
                print(" ".ljust(50), str(row[0]).ljust(14), row[1], sep="")
            input(ljust_enter)
        elif opt == 5:
            clear()
            print(reports_header)
            print("Player who places the lowest bet per game".center(140))
            query = "select lb.cardgame_id, p.player_id, lb.min_bet from (select cardgame_id, min(bet_points) as min_bet from player_game_round where bet_points is not null group by cardgame_id) as lb, player_game_round p where p.cardgame_id = lb.cardgame_id and  p.bet_points = lb.min_bet;"
            cursor.execute(query)
            result = cursor.fetchall()
            print(" ".ljust(50), "Game ID".ljust(14), "Player NIF".ljust(14), "Bet", sep="")
            for row in result:
                print(" ".ljust(50), str(row[0]).ljust(14), str(row[1]).ljust(14), row[2], sep="")
            input(ljust_enter)
        elif opt == 6:
            clear()
            print(reports_header)
            print("List of games won by Bots".center(140))
            query = "select pg.cardgame_id, w.win_pts, pg.player_id from (select cardgame_id, max(ending_points) as win_pts from player_game group by cardgame_id) as w, player_game pg, player p where pg.cardgame_id = w.cardgame_id and p.player_id = pg.player_id and  pg.ending_points = w.win_pts and p.human = 0;"
            cursor.execute(query)
            result = cursor.fetchall()
            print(" ".ljust(50), "Game ID".ljust(14), "Points".ljust(14), "Bot NIF", sep="")
            for row in result:
                print(" ".ljust(50), str(row[0]).ljust(14), str(row[1]).ljust(14), row[2], sep="")
            input(ljust_enter)
        elif opt == 7:
            clear()
            print(reports_header)
            print("Player who places the highest bet in each game".center(140))
            query = "select lb.cardgame_id, p.player_id, lb.max_bet from (select cardgame_id, max(bet_points) as max_bet from player_game_round where bet_points is not null group by cardgame_id) as lb, player_game_round p where p.cardgame_id = lb.cardgame_id and  p.bet_points = lb.max_bet;"
            cursor.execute(query)
            result = cursor.fetchall()
            print(" ".ljust(50), "Game ID".ljust(14), "Player NIF".ljust(14), "Bet", sep="")
            for row in result:
                print(" ".ljust(50), str(row[0]).ljust(14), str(row[1]).ljust(14), row[2], sep="")
            input(ljust_enter)
        elif opt == 0:
            return False

def getBBDDRanking():
    query = "SELECT * FROM player_earnings;"
    cursor.execute(query)
    result = cursor.fetchall()
    rank = {}
    for row in result:
        dict_aux = {"earnings": row[1], "games_played": row[2], "minutes_played": row[3]}
        rank[row[0]] = dict_aux
    return rank

def returnListRanking(rank, field="earnings"):
    listR = list(rank.keys())
    for pasada in range(len(listR) - 1):
        lista_ordenada = True
        for i in range(len(listR) - 1 - pasada):
            if rank[listR[i]][field] < rank[listR[i + 1]][field]:
                lista_ordenada = False
                aux = listR[i]
                listR[i] = listR[i + 1]
                listR[i + 1] = aux
        if lista_ordenada:
            break
    return listR

def ranking():
    while True:
        seq = "1)Players With More Earnings,2)Players With More Games Played,3)Players With More Minutes Played,4)Go back"
        opt = getOpt(func_text_opts(seq, ranking_header), "Option: ", [1, 2, 3, 4])
        clear()
        getPlayers()
        rank = getBBDDRanking()
        if opt == 1:
            listR = returnListRanking(rank)
            print(ranking_header)
            print(" " * 50, "Name".ljust(25), "Earnings".rjust(15))
            for i in listR:
                print(" "*50, players[i]["name"].ljust(25), str(rank[i]["earnings"]).rjust(15))
            input(ljust_enter)
        elif opt == 2:
            listR = returnListRanking(rank, "games_played")
            print(ranking_header)
            print(" " * 50, "Name".ljust(25), "Games Played".rjust(15))
            for i in listR:
                print(" " * 50, players[i]["name"].ljust(25), str(rank[i]["games_played"]).rjust(15))
            input(ljust_enter)
        elif opt == 3:
            listR = returnListRanking(rank, "minutes_played")
            print(ranking_header)
            print(" " * 50, "Name".ljust(25), "Minutes Played".rjust(15))
            for i in listR:
                print(" " * 50, players[i]["name"].ljust(25), str(rank[i]["minutes_played"]).rjust(15))
            input(ljust_enter)
        elif opt == 4:
            return False
