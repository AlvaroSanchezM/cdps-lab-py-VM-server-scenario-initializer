import sys
import logging
import os
import json

def jsonHandler_paraCadaOrden(): # 
        jsonCreado = os.path.isfile("gestiona-pc1.json")

        if jsonCreado:                             #YES => ver propiedad debug
                file = open('gestiona-pc1.json', 'r')
                data = json.load(file)
                #print("data = "+str(data))
                #num_serv = data['num_serv']
                #meter comprobación de si el json tiene variable debug dentro
                try: 
                        debug = data["debug"]                           #propiedad debug definida
                        print("data[debug] = "+str(debug))
                        #logging.debug(str(data))
                        if debug:                                       #debug:true => mostrar trazas
                                logging.basicConfig(level=logging.DEBUG)
                                #debug = "true"
                                logging.info("Debug = true")
                        else:                                           #else => no mostrar trazas
                                logging.basicConfig(level=logging.INFO)
                                #debug = "false"
                except KeyError:                     
                      logging.basicConfig(level=logging.INFO)
                      logging.info("No hay variable debug en el json")
                #logging.debug(str(data))
                #return num_serv
        else:
                logging.basicConfig(level=logging.INFO) #caMBIAR EN TODOS
                logging.info("No hay un archivo json creado aún") #caMBIAR EN TODOS
                #exit()

def gestionArgumentos():		#verifica que los argumentos que se introducen en el comando son válidos
    #logging.debug(str(sys.argv))

    jsonHandler_paraCadaOrden() #hace logging.config para todos
    longArgs = len(sys.argv)
    if longArgs < 2:
        return "\"No introducida\""
    if longArgs > 3:
        print("Error, demasiados argumentos introducidos.\n   Para ver como se usa el comando, escribir \"./gestiona-pc1 --help\"")
        exit()
    arg1 = sys.argv[0]
    arg2 = sys.argv[1]
    if arg2 == "create":
        if longArgs == 3:
            arg3 = sys.argv[2]
            try:
                numserv = int(arg3)
            except ValueError:
                print("Error, el argumento de la orden create debe ser un número entero, entre 1 y 5, incluidos.\n   Para ver como se usa el comando, escribir \"./gestiona-pc1 --help\"")
                exit()
            if numserv < 1 or numserv > 5:
                print("Error, el argumento de la orden create debe ser un número entre 1 y 5, incluidos.\n   Para ver como se usa el comando, escribir \"./gestiona-pc1 --help\"")
                exit()
            else:
                return "create"
        else:
            return "create"
    elif arg2 == "start":
        if longArgs > 2:
            print("Error, la orden \"start\" no necesita argumentos.\n   Para ver como se usa el comando, escribir \"./gestiona-pc1 --help\"")
            exit()
        else:
            return "start"
    elif arg2 == "stop":
        if longArgs > 2:
            print("Error, la orden \"stop\" no necesita argumentos.\n   Para ver como se usa el comando, escribir \"./gestiona-pc1 --help\"")
            exit()
        else:
            return "stop"
    elif arg2 == "destroy":
        if longArgs > 2:
            print("Error, la orden \"destroy\" no necesita argumentos.\n   Para ver como se usa el comando, escribir \"./gestiona-pc1 --help\"")
            exit()
        else:
            return "destroy"
    elif arg2 == "monitor":
        if longArgs == 3:
            arg3 = sys.argv[2]
            if arg3 == "-pers":
                if longArgs > 3:
                    print("Error, la orden \"monitor -pers\" no necesita más argumentos.\n   Para ver como se usa el comando, escribir \"./gestiona-pc1 --help\"")
                    exit()
                else:
                    return "monitorPers"
            else:
                print("Error, la orden \"monitor\" solo puede utilizar \"-pers\" como argumento.\n   Para ver como se usa el comando, escribir \"./gestiona-pc1 --help\"")
                exit()
        elif longArgs > 2:
            print("Error, la orden \"monitor\" solo utiliza la opción \"-pers\".\n   Para ver como se usa el comando, escribir \"./gestiona-pc1 --help\"")
            exit()
        else:
            return "monitor"
    elif arg2 == "--help":
        if longArgs > 2:
            print("La orden \"--help\" no necesita argumentos.\n")
        return "help"
    else:
        print("Error, argumento <orden> desconocido.\n   Para ver como se usa el comando, escribir \"./gestiona-pc1 --help\"")
        exit()
