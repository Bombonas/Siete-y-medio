from resources.funciones import *



menu00 = True
salir = False


while not salir:
    while menu00:
        option = getOpt(func_text_opts(opts_main, mainheader), opt_text, list(range(1, 7)))
