import logging
import os
import json

#nombresMaquinas = ["lb", "c1", "s1", "s2", "s3", "s4", "s5"]

def jsonHandler_paraCadaOrden(): # 
        jsonCreado = os.path.isfile("gestiona-pc1.json")

        if jsonCreado:                             #YES => ver propiedad debug
                file = open('gestiona-pc1.json', 'r')
                data = json.load(file)
                #print("data = "+str(data))
                num_serv = data['num_serv']
                #meter comprobación de si el json tiene variable debug dentro
                # try: 
                #         debug = data["debug"]                           #propiedad debug definida
                #         #logging.info("data[debug] = "+str(debug))
                #         #logging.debug(str(data))
                #         if debug:                                       #debug:true => mostrar trazas
                #                 logging.basicConfig(level=logging.DEBUG)
                #                 #debug = "true"
                #                 logging.info("Debug = true")
                #         else:                                           #else => no mostrar trazas
                #                 logging.basicConfig(level=logging.INFO)
                #                 #debug = "false"
                # except KeyError:
                #       logging.basicConfig(level=logging.INFO)
                #       logging.info("No hay variable debug en el json")
                #logging.debug(str(data))
                return num_serv
        else:
                logging.info("Error, las máquinas no han sido creadas aún. Ejecutar la orden create primero-")
                exit()

def modificaNombresMaquinas(nombresMaquinas):
        num_serv = jsonHandler_paraCadaOrden()
        numMaqFijo = 2 #marcamos como fijas las dos primeras maquinas del array, c1 y lb

        arrayRes = []
        for i in range(0,(numMaqFijo+num_serv)):
                arrayRes.append(nombresMaquinas[i])
        
        nombresMaquinas = arrayRes
        logging.info(str(nombresMaquinas))
        return nombresMaquinas

def stop(nombresMaquinas):
	logging.info("parando vms...")
	for nombreMaquina in nombresMaquinas:
		logging.info("parando maquina "+ nombreMaquina)
		os.system("sudo virsh shutdown "+nombreMaquina)

def parar(nombresMaquinas):
	nombresMaquinas = modificaNombresMaquinas(nombresMaquinas)
	stop(nombresMaquinas)

