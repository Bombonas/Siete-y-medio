from os import *
from resources.prints import *
from resources.bbdd_provisionales import *

def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')
