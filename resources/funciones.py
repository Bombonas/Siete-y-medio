import datetime
from os import *
from resources.prints import *
from resources.bbdd_provisionales import *
import random

def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

game = list(players)
def setGamePriority(mazo=[], jugadores=[]):
    cartasRepartidas = {}
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
            elif llista[j] == llista[j + 1] and cartas[cartasRepartidas[jugadores[j]]]['priority'] < cartas[cartasRepartidas[jugadores[j + 1]]]['priority']:
                jugadores[j], jugadores[j + 1] = jugadores[j + 1], jugadores[j]
    return jugadores

def resetPoints():
    for i in game:
        players[i]['points'] = 20

