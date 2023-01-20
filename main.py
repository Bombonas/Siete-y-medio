from resources.funciones import *
from resources.bbdd_provisionales import *


menu1 = False
menu11 = False
menu12 = False
menu13 = False

menu2 = False
menu21 = False
menu22 = False
menu23 = False

menu3 = False


menu4 = False
menu41 = False
menu42 = False
menu43 = False

menu5 = False

menu00 = True
salir = False


while not salir:
    while menu00:
        option = getOpt(func_text_opts(opts_main, mainheader), opt_text, list(range(1, 7)))
        if option == 1:
            menu1 = True
            menu00 = False
        elif option == 2:
            menu2 = True
            menu00 = False
        elif option == 3 and len(game) >= 2 and len(contextGame['deck']) == 3:
            menu3 = True
            menu00 = False
        elif option == 3 and len(game) >= 2:
            print(''.ljust(50) + 'Set the deck of cards first')
            input(enter)
        elif option == 3:
            print(''.ljust(50) + 'Set the players that compose the game first')
            input(enter)
        elif option == 4:
            menu4 = True
            menu00 = False
        elif option == 5:
            menu5 = True
            menu00 = False
        elif option == 6:
            input('Closing game. Press enter to Exit.')
            salir = True
            menu00 = False

    while menu1:
        option = getOpt(func_text_opts(opts_bbdd, bbddplayers), opt_text, list(range(1, 5)))
        if option == 1:
            menu11 = True
            menu1 = False
        elif option == 2:
            menu12 = True
            menu1 = False
        elif option == 3:
            menu13 = True
            menu1 = False
        elif option == 4:
            menu00 = True
            menu1 = False
















    while menu2:
        menu2 = settings()
        if menu2 == False:
            menu00 = True

    while menu21:
        pass





    while menu3:
        play_game()
        menu3 = False
        menu00 = True




    while menu4:
        option = getOpt(func_text_opts(opts_ranking, ranking), opt_text, list(range(1, 5)))
        if option == 1:
            menu41 = True
            menu4 = False
        elif option == 2:
            menu42 = True
            menu4 = False
        elif option == 3:
            menu43 = True
            menu4 = False
        elif option == 4:
            menu4 = False
            menu00 = True









    while menu5:
        pass