import datetime
import os
from resources.prints import *
from resources.bbdd_provisionales import *
import random
import math


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')



def setGamePriority(mazo=[], jugadores=[]):
    cartasRepartidas = {}
    cartasOrdenadas = {}
    for i in range(len(jugadores)):
        cartaRandom = random.choice(mazo)
        cartasRepartidas[jugadores[i]] = cartaRandom
        mazo.remove(cartaRandom)
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
        cartasOrdenadas.update({i: cartasRepartidas[i]})

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
    player_game.update({gameID:''})
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
    #Funcion que devuelve True si hay 2 o más jugadores con puntos, de lo contrario devuelve False

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
    #Funcion que crea una lista con los puntos de los jugadores y ordena la lista de jugadores de forma inversa segun sus puntos, pone la banca al principio
    #POST: Devuelve una lista con los ID_player ordenados.
    lista_puntos = []
    for i in game:
        lista_puntos.append(players[i]['points'])


    mida_llista = len(lista_puntos)

    for i in range(mida_llista - 1):
        for j in range(0, mida_llista - i - 1):
            if lista_puntos[j] > lista_puntos[j + 1]:
                lista_puntos[j], lista_puntos[j + 1] = lista_puntos[j + 1], lista_puntos[j]
                game[j], game[j + 1] = game[j + 1], game[j]

    for i in game:
        if players[i]['bank'] == True:
            game.remove(i)
            game.append(i)

    return game

def setBets():
    #Funcion que establece las apuestas según el tipo de jugador
    for i in game:
        if players[i]['points'] > 0:
            players[i]['bet'] = math.ceil(players[i]['points'] / 100 * players[i]['type'])

def standardRound(id, mazo=[]):
    tirada_cartas = []
    while True:
        if players[id]['bank'] == False:

            if players[id]['roundPoints'] == 0:
                nueva_carta = random.choice(mazo)
                mazo.remove(nueva_carta)
                tirada_cartas.append(nueva_carta)
                players[id]['roundPoints'] += cartas[nueva_carta]['realValue']
            else:
                if chanceExceedingSevenAndHalf(id, mazo) <= players[id]['type']:
                    nueva_carta = random.choice(mazo)
                    mazo.remove(nueva_carta)
                    tirada_cartas.append(nueva_carta)
                    players[id]['roundPoints'] += cartas[nueva_carta]['realValue']

                else:
                    return tirada_cartas
        else:
            if baknOrderNewCard(id) or chanceExceedingSevenAndHalf(id, mazo) <= players[id]['type']:
                nueva_carta = random.choice(mazo)
                mazo.remove(nueva_carta)
                tirada_cartas.append(nueva_carta)
                players[id]['roundPoints'] += cartas[nueva_carta]['realValue']

            else:
                return tirada_cartas

def getOpt(textOpts="",inputOptText="",rangeList=[],exceptions=[]):
    # PRE:  Al parámetro textOpts se le pasa el string con las opciones del manú
    #       Al parámetro inputOpt se le pasa el string con la frase que pide que escojamos una opción
    #       El parámetro RangeList contiene las opciones contempladas por el menu
    #       El parámetro exceptions contiene las posibles excepciones que pueden generarse
    # POST: Devolverá un valor de RangeList si la selección es correcta y devolverá un valor de exceptions si ha ocurrido
    #       un error
    correct = False
    opc = ''
    input_text = ''.ljust(50) + inputOptText
    while not correct:
        clear()
        print(textOpts)
        opc = input(input_text)
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
    # Llamamos a una funcion que pida los DNIs y calcule los puntos que tiene un jugador a la BBDD,
    # y los devuelva en formato diccionario; dni : puntos

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

def chanceExceedingSevenAndHalf(id, mazo):
    bad_cards = 0
    for i in mazo:
        if cartas[i]["realValue"] + players[id]["roundPoints"] > 7.5:
            bad_cards += 1

    return (bad_cards * 100) / len(mazo)

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
                if(players[i]["roundPoints"] <= 7.5 and players[i]["roundPoints"] <= players[id]["roundPoints"]) or players[i]["roundPoints"] > 7.5:
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
        rounds = input("Max Rounds : ")
        if not rounds.isdigit():
            print("Please, only introduce numbers")
        elif int(rounds) <= 0:
            print("Please, introduce a number bigger than 0")
        else:
            correct = True
    contextGame["maxRounds"] = rounds



# USAR UNA FUNCION PARA CADA COSA, QUE NO DEJE SALIR HASTA QUE HAYAN 2 PLAYERS EN "GAME" Y UNA BARAJA ESCOGIDA,
# DEFAULT ROUND SETTINGS = 5
def settings():
    option = getOpt(func_text_opts(opts_settings, settings_print), opt_text, list(range(1, 5)))
    if option == 1:
        setPlayersGame()
    elif option == 2:
        menu22 = True
        menu2 = False
    elif option == 3:
        menu23 = True
        menu2 = False
    elif option == 4:
        menu2 = False
        menu00 = True

def setPlayersGame():
    actualPlayers = setgameplayers + '\n'*3 + '*************** Actual Players In Game ***************'.center(140) + '\n'
    tabla_jugadores = set_game_players_cabecera
    bots = []
    humans = []
    if len(game) == 0:
        actualPlayers += 'There is no players in game'.center(140)
    else:
        for i in game:
            actualPlayers += str(i).center(140)
    print(actualPlayers)
    input(enter)

    for i in players:
        if players[i]['human'] == True:
            humans.append(i)
        else:
            bots.append(i)
    # Crear tabla de players
def newRandomDNI():
    DNI = random.randint(10000000, 99999999)
    letra = letrasDni[DNI % 23]
    DNI = str(DNI) + letra.upper()
    return DNI

def setNewPlayer(human=True):
    dni = ""
    profile = 0
    name = ""
    if human:
        dni = nif_validator()
    else:
        dni = newRandomDNI()

    opt = getOpt("Select your Profile:\n1)Cautious\n2)Moderated\n3)Bold", "Option", [1, 2, 3])
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
