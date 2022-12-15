import logging
import os
import json



def jsonHandler_paraCadaOrden(): # 
        jsonCreado = os.path.isfile("gestiona-pc1.json")

        if jsonCreado:                             #YES => ver propiedad debug
                file = open('gestiona-pc1.json', 'r')
                data = json.load(file)
                #logging.debug("data = "+str(data))
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
                logging.debug(str(data))
                return num_serv
        else:
                print("Error, las máquinas no han sido creadas aún. Ejecutar la orden create primero-")
                exit()

def modificaNombresMaquinas(nombresMaquinas):
        num_serv = jsonHandler_paraCadaOrden()
        numMaqFijo = 2 #marcamos como fijas las dos primeras maquinas del array, c1 y lb

        arrayRes = []
        for i in range(0,(numMaqFijo+num_serv)):
                arrayRes.append(nombresMaquinas[i])
        
        nombresMaquinas = arrayRes
        logging.debug(str(nombresMaquinas))
        return nombresMaquinas

def destroy(nombresMaquinas):

        os.system("pwd > log.txt")

        fileread = open('log.txt', 'r')
        for line in fileread:
                logging.debug("pwd = " + line+"/")
                pwd = line
        fileread.close()

        res = pwd.split("\n")
        logging.debug(str(res))
        origen = "".join(res)+"/"
        logging.debug("pwd="+pwd)

        os.system("rm log.txt")

        logging.info("eliminando vms...")
        for nombreMaquina in nombresMaquinas:
                logging.info("eliminando maquina "+ origen+nombreMaquina)
                os.system("sudo virsh destroy "+nombreMaquina)
                os.system("sudo virsh undefine "+nombreMaquina)

        os.system("sudo ifconfig LAN1 down") #detenemos LAN1
        os.system("sudo ifconfig LAN2 down") 
        os.system("sudo brctl delbr LAN1") 
        os.system("sudo brctl delbr LAN2")
        logging.info("LAN1 y LAN2 se detuvieron con exito")    

        for nombreMaquina in nombresMaquinas:
                logging.info("eliminando qcow2 "+ origen+nombreMaquina)
                os.system("rm "+origen+nombreMaquina+".qcow2 -f")
                os.system("rm "+origen+nombreMaquina+".xml -f")

        os.system("rm -f gestiona-pc1.json")

        os.system("ps -au > procesos.txt")      #Cierra la ventana del monitor
        proc = open('procesos.txt', 'r')
        for line in proc:
                if "watch -n 0,5 sudo virsh list --all" in line and (not "xterm" in line):
                        arr = line.split(" ")
                        logging.debug(str(arr))
                        pid = arr[1]
                        i=1
                        while pid == "":
                                logging.debug("i = "+str(i)+", pidVacio")
                                pid = arr[1+i]
                                i=i+1
                        logging.debug(line)
                        logging.debug("pidFinal = "+str(pid))
                        os.system("kill "+ str(pid))
        proc.close()
        os.system("rm -f procesos.txt")
        logging.info("ventanas monitorizadas cerradas")

def borrar(nombresMaquinas):
	#nombresMaquinas = ["lb", "c1", "s1", "s2", "s3", "s4", "s5"]
	nombresMaquinas = modificaNombresMaquinas(nombresMaquinas)
	destroy(nombresMaquinas)
