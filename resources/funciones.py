from resources.bbdd_provisionales import *
from resources.prints import *
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


