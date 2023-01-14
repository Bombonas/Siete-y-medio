from resources.bbdd_provisionales import *
from resources.prints import *
import random
import mysql.connector

db = mysql.connector.connect(user="MAP", password="2023Proyecto",
                                   host="proyecto1.mysql.database.azure.com",
                                   database="seven_and_half",
                                   port="3306")

cursor = db.cursor()

def getOpt(textOpts="",inputOptText="",rangeList=[],exceptions=[]):
    # PRE:  Al parámetro textOpts se le pasa el string con las opciones del manú
    #       Al parámetro inputOpt se le pasa el string con la frase que pide que escojamos una opción
    #       El parámetro RangeList contiene las opciones contempladas por el menu
    #       El parámetro exceptions contiene las posibles excepciones que pueden generarse
    # POST: Devolverá un valor de RangeList si la selección es correcta y devolverá un valor de exceptions si ha ocurrido
    #       un error
    correct = False
    opc = ''
    while not correct:
        print(textOpts)
        opc = input(inputOptText)
        try:
            opc = int(opc)
            if opc not in rangeList and opc not in exceptions:
                raise TypeError('Incorrect Option')
            else:
                correct = True
        except ValueError:
            print('Please, introduce only numbers')
            input("Enter to continue")
        except TypeError as e:
            print(e)
            input("Enter to continue")
    return opc

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

def baknOrderNewCard(id, game):
        earnings = 0
        looses = 0
        ret = True
        for i in game:
            if i != id:
                if(players[i]["roundPoints"] <= 7.5 and players[i]["roundPoints"] <= players[id]["roundPoints"]) or players[i]["roundPoints"] > 7.5:
                    earnings += players[i]["bet"]
                else:
                    if players[i]["roundPoints"] == 7.5:
                        looses += players[i]["bet"] * 2
                    else:
                        looses += players[i]["bet"]
        if earnings > looses:
            ret = False

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

def settings():
    menu = "1)Set Game\n2)Set Card's Deck\n3)Set Max Rounds(Default 5 Rounds)\n4)Go back"
    opt = getOpt(menu, "Option: ", [1, 2, 3, 4])
    if opt == 1:
        print("opt1")
    elif opt == 2:
        print("opt2")
    elif opt == 3:
        setMaxRounds()
    elif opt == 4:
        print("opt4")

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
    insert = "INSERT INTO player (player_id, player_name, player_risk, human) VALUES (%s,%s,%s,%s)"
    cursor.execute(insert, tup_player)
    db.commit()

def newPlayer(dni, name, profile, human):
    dic_aux = {"name": name, "human": human, "bank": False, "initialCard": "", "priority": 0, "type": profile,
               "bet": 4, "points": 0, "cards": [], "roundPoints": 0}
    return (dni, dic_aux)


def showhPlayersGame():
    print("Actual Players In Game".center(60, "*"))
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
            print(p)
        print()
    else:
        print("There is no players in game")
    input("Enter to continue".center(60))

def showhPlayersBBDD():
    bots = []
    humans = []
    for id in players:
        if players[id]["human"]:
            humans.append(id)
        else:
            bots.append(id)
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
    showhPlayersGame()
    while(input("")):
        pass

showhPlayersBBDD()