import datetime
import os
from prints import *
from bbdd_provisionales import *
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

def chanceExceedingSevenAndHalf(id, mazo):
    bad_cards = 0
    for i in mazo:
        if cartas[i]["realValue"] + players[id]["roundPoints"] > 7.5:
            bad_cards += 1

    return (bad_cards * 100) / len(mazo)

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
    ret = 0
    # Funcion que devuelve True si hay 2 o más jugadores con puntos, de lo contrario devuelve False
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
        print("DNI:", dni)

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
    savePlayer((dni, name, profile, human))

def savePlayer(tup_player):
    query = "INSERT INTO player (player_id, player_name, player_risk, human) VALUES (%s,%s,%s,%s)"
    cursor.execute(query, tup_player)
    db.commit()

def newPlayer(dni, name, profile, human):
    dic_aux = {"name": name, "human": human, "bank": False, "initialCard": "", "priority": 0, "type": profile,
               "bet": 4, "points": 0, "cards": [], "roundPoints": 0}
    return (dni, dic_aux)


def showhPlayersGame():
    print(" "*40, "Actual Players In Game".center(60, "*"), sep="")
    if len(game) > 0:
        for id in game:
            p = id.ljust(15) + " "*3 + players[id]["name"].ljust(18) + " "*2
            if players[id]["human"]:
                p += "human".rjust(7)
            else:
                p += "bot".rjust(7)
            p += " "*3
            if players[id]["type"] == 30:
                p += "Cautious"
            elif players[id]["type"] == 40:
                p += "Moderated"
            elif players[id]["type"] == 50:
                p += "Bold"
            print(" "*40, p, sep="")
        print()
    else:
        print(" "*40, "There is no players in game", sep="")
    print(" "*40, "Enter to continue".center(60), sep="")
    input()

def orderAllPlayers():
    # Funcion que crea una lista con los puntos de los jugadores y ordena la lista de jugadores de forma inversa segun sus puntos, pone la banca al principio
    # POST: Devuelve una lista con los ID_player ordenados.
    lista_puntos = []
    for i in game:
        lista_puntos.append(players[i]['points'])

    mida_llista = len(lista_puntos)

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

def setPlayersGame():
    clear()
    showhPlayersGame()
    while True:
        clear()
        showhPlayersBBDD()
        opt = input("Option (id to add to game, -id to remove player, sh to show actual players in game, -1 to go back: ")
        try:
            if len(opt) < 2:
                raise TypeError()
            elif opt[0] == "-":
                if opt[1] == "1" and len(opt) == 2:
                    clear()
                    break
                elif len(opt) == 10 and opt[1:] in game:
                    game.remove(opt[1:])
                    showhPlayersGame()
                else:
                    raise TypeError
            elif opt == "sh":
                showhPlayersGame()
            elif len(opt) == 9 and opt in list(players.keys()):
                game.append(opt)
                showhPlayersGame()
            else:
                raise TypeError

        except TypeError:
            print("Invalid Option".center(140, "="))
            print(" " * 40, "Enter to continue".center(60), sep="")
            input("")


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

def removeBBDDPlayer():
    while True:
        clear()
        showhPlayersBBDD()
        opt = input("Option (-id to remove player, -1 to go back): ")
        try:
            if len(opt) < 2:
                raise TypeError()
            elif opt[0] == "-":
                if opt[1] == "1" and len(opt) == 2:
                    clear()
                    break
                elif len(opt) == 10 and opt[1:] in list(players.keys()):
                    print(opt[1:])
                    input()
                    delBBDDPlayer(opt[1:])
                else:
                    raise TypeError()
            else:
                raise TypeError()
        except TypeError:
            print("Invalid Option".center(140, "="))
            print(" " * 40, "Enter to continue".center(60), sep="")
            input("")

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

def tipo_de_riesgo(id):
    riesgo = ''
    if players[id]['type'] == 30:
        riesgo = 'Cautious'
    elif players[id]['type'] == 40:
        riesgo = 'Moderated'
    elif players[id]['type'] == 50:
        riesgo = 'Bold'

    return riesgo

# USAR UNA FUNCION PARA CADA COSA, QUE NO DEJE SALIR HASTA QUE HAYAN 2 PLAYERS EN "GAME" Y UNA BARAJA ESCOGIDA,
# DEFAULT ROUND SETTINGS = 5
def settings():
    while True:
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
            return False

def getPlayers():
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
    insert = "DELETE FROM player WHERE player_id = '" + nif + "';"
    cursor.execute(insert)
    db.commit()




def printStats(titulo=""):
    # PREGUNTAR LAS VARIABLES
    print(titulo.center(140, "*"))
    lista = ["Name", "Human", "Priority", "Type", "Bank", "Bet", "Points", "Cards", "Roundpoints"]
    arguments = ["name", "human", "priority", "type", "bank", "bet", "points", "cards", "roundPoints"]
    for i in range(0, 8):
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



def getBBDDRanking():
    return

def reports():
    # MIRAR EL NUEVO getOpt
    return

def returnListRanking(field="earnings"):
    return

def setCardsDeck():
    return














