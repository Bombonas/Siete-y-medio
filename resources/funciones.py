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
    # Devolvemos una lista de tuplas con (DNI, CARTA)
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
    for i in game:
        players[i]['points'] = 20


def generate_game_id():
    new_cardgame_id = len(cardgame_ids)
    return new_cardgame_id


def card_id_list(diccionario):
    lista_card_id = []
    for i in diccionario:
        lista_card_id.append(diccionario[i])

    return lista_card_id


def fill_player_game(gameID, jugadores=[], card_id_list=[], starting_points_list=[], ending_points_list=[]):
    player_game.update({gameID: ''})
    for i in range(len(jugadores)):
        if i == 0:
            player_game[gameID] = {jugadores[i]: {'initial_card_id': card_id_list[i], 'starting_points':
                starting_points_list[i], 'ending_points': ending_points_list[i]}}
        else:
            player_game[gameID][jugadores[i]] = {'initial_card_id': card_id_list[i], 'starting_points':
                starting_points_list[i], 'ending_points': ending_points_list[i]}
    return player_game


# fill_player_game(generate_game_id(), list(setGamePriority(list(cartas), list(players))), card_id_list(setGamePriority(list(cartas), list(players))),
#                  [20,20,20,20], [3, 1, 45, 0])

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
        if players[i]['points'] > 0:
            players[i]['bet'] = math.ceil(players[i]['points'] / 100 * players[i]['type'])


def standardRound(id, mazo1):

    tirada_cartas = []
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
            if baknOrderNewCard(id) or chanceExceedingSevenAndHalf(id, mazo1) <= players[id]['type']:
                nueva_carta = random.choice(mazo1)
                mazo1.remove(nueva_carta)
                tirada_cartas.append(nueva_carta)
                players[id]['roundPoints'] += cartas[nueva_carta]['realValue']

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
        seq = ''
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
    print("Stats of {}".format(players[id]["name"]).center(140, "*"))
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


def addRemovePlayers():
    menu = "1)New Human Player\n2)New Bot\n3)Show/Remove Players\n4)Go back"
    opt = getOpt(menu, "Option: ", [1, 2, 3, 4])
    if opt == 1:
        print("opt1")
    elif opt == 2:
        print("opt2")
    elif opt == 3:
        print("opt3")
    elif opt == 4:
        print("opt4")


def setMaxRounds():
    correct = False
    rounds = 5
    while not correct:
        clear()
        print(setmaxrounds)
        rounds = input(''.ljust(60)+"Max Rounds: ")
        if not rounds.isdigit():
            print(''.ljust(60)+"Please, only introduce numbers")
            input(''.ljust(60)+'Enter to continue')
        elif int(rounds) <= 0:
            print(''.ljust(60)+"Please, introduce a number bigger than 0")
            input(''.ljust(60)+'Enter to continue')
        else:
            correct = True

            print(''.ljust(60)+'Established maximum of rounds to', rounds)
            input(''.ljust(60)+'Enter to continue')
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

#editar para evitar que se repitan dnis
def newRandomDNI():
    correct = False
    DNI = ''
    while correct:
        DNI = random.randint(10000000, 99999999)
        letra = letrasDni[DNI % 23]
        DNI = str(DNI) + letra.upper()
        if DNI not in list(players):
            correct = True

    return DNI


def setNewPlayer(human=True):
    dni = ""
    profile = 0
    name = ""
    if human:
        dni = nif_validator()
    else:
        dni = newRandomDNI()

    opt = getOpt("Select your Profile:,1)Cautious,2)Moderated,3)Bold", "Option", [1, 2, 3])
    if opt == 1:
        profile = 30
    elif opt == 2:
        profile = 40
    else:
        profile = 50

    correct = False
    while not correct:
        name = input("Name: ")
        if not name.isalnum():
            print("Incorrect name, please, enter a name not empty with only letters")
        else:
            correct = True
    tup_player = newPlayer(dni, name, profile, human)


def newPlayer(dni, name, profile, human):
    dic_aux = {"name": name, "human": human, "bank": False, "initialCard": "", "priority": 0, "type": profile,
               "bet": 4, "points": 0, "cards": [], "roundPoints": 0}
    return (dni, dic_aux)


def printStats(titulo=""):
    # PREGUNTAR LAS VARIABLES
    print(titulo.center(140, "*"))
    lista = ["Name", "Human", "Priority", "Type", "Bank", "Bet", "Points", "Cards", "Roundpoints"]
    arguments = ["name", "human", "priority", "type", "bank", "bet", "points", "cards", "roundPoints"]
    for i in range(0, 9):
        seq = lista[i].ljust(20) + " "*5
        for j in game:
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
#COPIAR DE GITHUB DE PABLO
def set_card_deck():
    opt = getOpt(func_text_opts('1) ESP,2) POK,0) Go Back', deckofcards), 'Option: ', [0, 1, 2])
    if opt == 1:
        contextGame['deck'] = 'ESP'
        #IMPORTAR MAZO DETERMINADO A CARTAS
        print('Established Card Deck ESP, Baraja Española')
        input(''*50+'Enter to continue')

    elif opt == 2:
        contextGame['deck'] = 'POK'
        #IMPORTAR MAZO DETERMINADO A CARTAS
        print('Established Card Deck POK, Poker Deck')
        input(''*50+'Enter to continue')

    elif opt == 0:
        print('Deck not chosen.')
        input(enter)


def distributionPointAndNewBankCandidates(banco, sorted_players_main=[]):
    # SUSTITUIR CODIGO DE JUEGO ACTUAL POR ESTA FUNCION

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


# USAR UNA FUNCION PARA CADA COSA, QUE NO DEJE SALIR HASTA QUE HAYAN 2 PLAYERS EN "GAME" Y UNA BARAJA ESCOGIDA,
# DEFAULT ROUND SETTINGS = 5
def settings():
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
    for i in game:
        players[i]['roundPoints'] = 0
        players[i]['cards'] = []


def play_game():
    resetPoints()
    banca_debe = 0
    banca = ''
    order = setGamePriority(list(cartas), game)
    jugadores_ordenados = []
    priority = 0
    for i in order:
        jugadores_ordenados.append(i[0])
        priority += 1
        players[i[0]]['priority'] = priority
        players[i[0]]['initialCard'] = i[1]
        if priority == 1:
            banca = i[0]
            players[i[0]]['bank'] = True

    for i in range(0, contextGame['maxRounds']):
        print(i)
        mazo = list(cartas)
        print(game)
        reset_stats()
        setBets()

        printStats()

        input('asdasd')
        jugadores_ordenados = orderAllPlayers()
        #ORDENAR JUGADORES EN JUGADORES_ORDENADOS CADA RONDA
        for jugador in jugadores_ordenados:
            # Si es humano, mostrar menu game
            players[jugador]['cards'] = (standardRound(jugador, mazo))
            print(players[jugador]['cards'])

        distributionPointAndNewBankCandidates(banca, jugadores_ordenados)

        for j in game:
            if players[j]['bank'] is True:
                banca = j

        if not checkMinimun2PlayerWithPoints():
            break

        printStats()
        print(game)
        input('asdasd')
    print(gameover)
    game.clear()
    print(game)
    input(enter)

