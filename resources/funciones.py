import datetime
import os
from resources.prints import *
from resources.bbdd_provisionales import *
import random
import math
import itertools


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def setGamePriority(mazo=[], jugadores=[]):
    # PRE: Introducimos la list(cartas) y la game=[]
    # Repartimos una carta a cada uno
    # Creamos otra lista en el mismo orden con los valores de las cartas para ordenarlas
    # Devolvemos una lista de tuplas con (DNI, CARTA)
    cartasRepartidas = {}
    cartasOrdenadas = []
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
        cartasOrdenadas.append((i, cartasRepartidas[i]))

    return cartasOrdenadas
# print(setGamePriority(list(cartas), list(players)))

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
    # Funcion que crea una lista con los puntos de los jugadores y ordena la lista de jugadores de forma inversa segun sus puntos, pone la banca al principio
    # POST: Devuelve una lista con los ID_player ordenados.
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
    # Funcion que establece las apuestas según el tipo de jugador
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


def getOpt(textOpts="", inputOptText="", rangeList=[], exceptions=[]):
    # PRE:  Al parámetro textOpts se le pasa el string con las opciones del menú
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
    contextGame["maxRounds"] = rounds


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


#editar para evitar que se repitan dnis
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


#VINCULAR DECK CON LA VARIABLE QUE USAREMOS PARA ESTABLECER EL DECK
def set_card_deck():
    opt = getOpt(func_text_opts('1) ESP,2) POK,0) Go Back', deckofcards), 'Option: ', [0, 1, 2])
    if opt == 1:
        contextGame['deck'] = 'ESP'
        print('Established Card Deck ESP, Baraja Española')
        input(''*50+'Enter to continue')
    elif opt == 2:
        contextGame['deck'] = 'POK'
        print('Established Card Deck POK, Poker Deck')
        input(''*50+'Enter to continue')

    elif opt == 3:
        print('Deck not chosen.')
        input(enter)
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

def play_game():
    resetPoints()

    order = setGamePriority(list(cartas), list(players))
    priority = 0
    for i in order:
        priority += 1
        players[i[0]]['priority'] = priority
        players[i[0]]['initialCard'] = i[1]
        if priority == 1:
            players[i[0]]['bank'] = True
