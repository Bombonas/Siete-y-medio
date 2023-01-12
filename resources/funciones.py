import datetime
from os import *
from resources.prints import *
from resources.bbdd_provisionales import *
import random
import math

def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


game = list(players)


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
print(orderAllPlayers())
def setBets():
    #Funcion que establece las apuestas según el tipo de jugador
    for i in game:
        if players[i]['points'] > 0:
            players[i]['bet'] = math.ceil(players[i]['points'] / 100 * players[i]['type'])

def standardRound(id, mazo=[]):
    pass