from subprocess import call
import sys
import os
import xml.etree.ElementTree as ET
import logging
import json




def jsonGestor(): #Solo para la orden create

        print(sys.argv)
        #jsonCreado = 1

        jsonCreado = os.path.isfile("gestiona-pc1.json")  #ver si ya hay un json creado

        if jsonCreado:                             #YES => ver propiedad debug
                file = open('gestiona-pc1.json', 'r')
                data = json.load(file)
                #logging.info("data = "+str(data))
                #num_serv = data['num_serv']
                #meter comprobación de si el json tiene variable debug dentro
                try: 
                        debug = data["debug"]                           #propiedad debug definida
                        print("data[debug] = "+str(debug))
                        data = {"num_serv": 2, "debug": debug}          #definir formato json con num_serv por defecto
                        print(str(data))
                        if debug:                                       #debug:true => mostrar trazas
                                #logging.basicConfig(level=logging.DEBUG)

                                debug = "true"
                        else:                                           #else => no mostrar trazas
                                #logging.basicConfig(level=logging.INFO)
                                debug = "false"
                except KeyError:                     
                      #logging.basicConfig(level=logging.INFO)
                      logging.debug("No hay variable debug en el json")
                logging.debug(str(data))
                logging.debug("modo debug activado ==**==**??")
                logging.info("modo debug desactivado *******")
                
        else:                                           #NO => definir formato json con num_serv por defecto
                data = {"num_serv": 2}

        #meter dentro de gestiona-pc1Temp.json el valor de num_serv pasado
        if len(sys.argv) > 2:  #1º verificar si se da un 2º input además de la orden
                try:
                        int(sys.argv[2])
                except ValueError:
                        logging.info("Error: valor input2 = numero de servidores, debe ser un **número entero** entre 1 y 5")
                        exit()
                if int(sys.argv[2]) >= 1 and int(sys.argv[2]) <= 5: #YES => 2º verificar si es entero perteneciente al rango permitido
                        data["num_serv"] = int(sys.argv[2])                      #YES => meter en num_servers en el json
                else:                                                   #NO => sacar error y terminar programa
                        logging.info("Error: valor input2 = numero de servidores, debe ser un número entero **entre 1 y 5**")
                        exit()
        #else:                                                   #NO => dejar num_serv: 2 por defecto
                #data["num_serv"] = 2

        logging.debug(str(data))

        with open('gestiona-pc1Temp.json', 'w') as fileB:#crear gestiona-pc1Temp.json
                texto = "\"".join(str(data).split("\'"))
                if "F" in texto:                    #Parche de error raro entre valores booleanos de Python y json
                        res = "f".join(texto.split("F"))
                elif "T" in texto:
                        res = "t".join(texto.split("T"))
                else:
                        res = texto
                fileB.write(res)              #Rellenar gestiona-pc1Temp.json con los datos obtenidos hasta ahora
        fileB.close()
        num_serv = data['num_serv']
        return num_serv




def modificaNombresMaquinas(nombresMaquinas):
        num_serv = jsonGestor()
        numMaqFijo = 2 #marcamos como fijas las dos primeras maquinas del array, c1 y lb

        arrayRes = []
        for i in range(0,(numMaqFijo+num_serv)):
                arrayRes.append(nombresMaquinas[i])
        nombresMaquinas = arrayRes
        logging.info("\nnombreMaquinas = " + str(nombresMaquinas))
        return nombresMaquinas


def existeArchivoBase(): #Solo para la orden create
        try:    #verificar que existe el archivo base de qcows de MVs del escenario
                file1 = open('cdps-vm-base-pc1.qcow2', 'r')
                file1.close()
        except FileNotFoundError:
                logging.info("\nError: no se encontró el archivo \"cdps-vm-base-pc1.qcow2\" en el fichero actual\n")
                #Si ya existía json, borrar los cambios (borrar la copia antes de hacer "mv gestiona-pc1Temp.jason gestiona-pc1.jason")
                os.system("rm gestiona-pc1Temp.json -f")
                exit()

        try:    #verificar que existe el archivo base de MVs del escenario
                file1 = open('plantilla-vm-pc1.xml', 'r')
                file1.close()
        except FileNotFoundError:
                logging.info("\nError: no se encontró el archivo \"plantilla-vm-pc1.xml\" en el fichero actual\n")
                #Si ya existía json, borrar los cambios (borrar la copia antes de hacer "mv gestiona-pc1Temp.jason gestiona-pc1.jason")
                os.system("rm gestiona-pc1Temp.json -f")
                exit()
        os.system("mv gestiona-pc1Temp.json gestiona-pc1.json -f")


def createqcows(nombresMaquinas):
        for i in range(len(nombresMaquinas)):
                nomMaq = "".join([nombresMaquinas[i], ".qcow2"])
                call(["qemu-img", "create", "-f", "qcow2", "-b", "cdps-vm-base-pc1.qcow2", nomMaq])
                logging.debug("\ncreado qcow: "+nomMaq)


def createxml(nombresMaquinas):
        #Primero se obtiene el nombre de la carpeta en la que se está ejecutando el script
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
        logging.debug("\nSe está ejecutando el script en:" + origen + "/")
# Cargamos el fichero xml
        for nombres in nombresMaquinas:
                tree = ET.parse('plantilla-vm-pc1.xml')
                root = tree.getroot()

                for name in root.iter('name'):
                        name.text = nombres      
    
                if nombres == "s1" or nombres == "s2" or nombres == "s3" or nombres == "s4" or nombres == "s5":
                        logging.debug("modificando "+ nombres)
                        source = root.find("./devices/interface/source")
                        source.set("bridge", "LAN2")
                        disk = root.find("./devices/disk/source")
                        disk.set("file", origen+nombres+".qcow2") 

                elif nombres == "c1":
                        logging.debug("modificando "+ nombres)
                        source = root.find("./devices/interface/source")
                        source.set("bridge", "LAN1")
                        disk = root.find("./devices/disk/source")
                        disk.set("file", origen+nombres+".qcow2") 

                elif nombres == "lb":
                        logging.debug("modificando "+ nombres)
                        source = root.find("./devices/interface/source")
                        source.set("bridge", "LAN1")
                        interface = ET.Element("interface", type = "bridge")
                        devices = root.find("devices")
                        devices.append(interface)
                        source = ET.Element("source", bridge = "LAN2")
                        model = ET.Element("model", type = "virtio")
                        interface.append(source)
                        interface.append(model)
                        source = root.find("./devices/interface/source")
                        disk = root.find("./devices/disk/source")
                        disk.set("file", origen+nombres+".qcow2")  
        
        
        
                tree.write(nombres+'.xml')  



def createbridges():
    call(["sudo", "brctl", "addbr", "LAN1"])
    call(["sudo", "brctl", "addbr", "LAN2"])
    call(["sudo", "ifconfig", "LAN1", "up"])
    call(["sudo", "ifconfig", "LAN2", "up"])

def definevm(nombresMaquinas):
    for nombreMaquina in nombresMaquinas:    
            #definimos cada maquina
            os.system("sudo virsh define "+nombreMaquina+".xml")


def createhostnames(nombresMaquinas):
    #directorio temporal en el host
    os.system("mkdir temporal")
    os.system("cd temporal")
    for nombreMaquina in nombresMaquinas: 
    #creamos fichero hostname y lo sustituimos por el de la mv            
            os.system("echo "+nombreMaquina+" > hostname")
            fhostname = open("hostname", "w")
            fhostname.write(nombreMaquina)
            fhostname.close()               
            os.system("sudo virt-copy-in -a " + nombreMaquina + ".qcow2 hostname /etc")
            os.system("rm hostname")
            logging.debug("hostname maquina"+nombreMaquina+"creado")
    os.system("cd ..")


def createhosts(nombresMaquinas):

        for nombreMaquina in nombresMaquinas:
                #obtenemos fichero hosts de la mv lo cambiamos y sustituimos
                os.system("sudo virt-copy-out -a"+nombreMaquina+".qcow2 /etc/hosts .")
                fin = open("hosts","r")
                fout = open("hostscopia", "w")
                for line in fin:
                        if "127.0.1.1 " in line:
                                fout.write("127.0.1.1 "+nombreMaquina+"\n")
                        else:
                                fout.write(line)
                fin.close()
                fout.close()
                os.system("mv hostscopia hosts -f")
                #copiamos hosts de la carpeta temporal y lo copiamos a las mv
                os.system("sudo virt-copy-in -a " + nombreMaquina + ".qcow2 hosts /etc")
                os.system("rm hosts")
   
def createinterfaces(nombresMaquinas):
        #crea un fichero nuevo en el directorio temporal del host para cada mv y luego lo sustituye en cada mv
        for nombreMaquina in nombresMaquinas:
                finterfaces = open("interfacestemp", "w")
                finterfaces.write("auto lo\n")
                finterfaces.write("iface lo inet loopback\n")
                finterfaces.write("\n")
                finterfaces.write("auto eth0\n")
                finterfaces.write("iface eth0 inet static\n")
                if nombreMaquina == "s1":
                        finterfaces.write(" address 10.20.2.101\n")                      
                elif nombreMaquina == "s2":
                        finterfaces.write(" address 10.20.2.102\n")                    
                elif nombreMaquina == "s3":
                        finterfaces.write(" address 10.20.2.103\n")
                elif nombreMaquina == "s4":
                        finterfaces.write(" address 10.20.2.104\n")
                elif nombreMaquina == "s5":
                        finterfaces.write(" address 10.20.2.105\n")
                elif nombreMaquina == "lb":
                        finterfaces.write(" address 10.20.1.1\n")
                        finterfaces.write(" netmask 255.255.255.0\n")
                        finterfaces.write(" gateway 10.20.1.1\n")
                        finterfaces.write("auto eth1\n")
                        finterfaces.write("iface eth1 inet static\n")
                        finterfaces.write(" address 10.20.2.1\n")
                        finterfaces.write(" netmask 255.255.255.0\n")
                        finterfaces.write(" gateway 10.20.2.1\n")
                elif nombreMaquina == "c1":
                        finterfaces.write(" address 10.20.1.2\n")
                        finterfaces.write(" netmask 255.255.255.0\n")
                        finterfaces.write(" gateway 10.20.1.1\n")
                if "s" in nombreMaquina:
                        finterfaces.write(" netmask 255.255.255.0\n")
                        finterfaces.write(" gateway 10.20.2.1\n")
                finterfaces.close()
                os.system("mv interfacestemp interfaces -f")     
                os.system("sudo virt-copy-in -a " + nombreMaquina + ".qcow2 interfaces /etc/network")
                os.system("rm interfaces")
                os.system("rm -Rf temporal")             

def editlbsysctl():
        os.system("sudo virt-edit -a lb.qcow2 /etc/sysctl.conf \-e 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/'")

def confighost():
        os.system("sudo ifconfig LAN1 10.20.1.3/24")
        os.system("sudo ip route add 10.20.0.0/16 via 10.20.1.1")


#main
#jsonGestor()
#print("\n--------------Fichero json checkeado y modificado")
def crear(nombresMaquinas):
        #nombresMaquinas = ["lb", "c1", "s1", "s2", "s3", "s4", "s5"]
        nombresMaquinas = modificaNombresMaquinas(nombresMaquinas)
        logging.info("\n--------------Numero de servidores ajustado")
        existeArchivoBase()
        logging.info("\n--------------Verificada existencia de arch base qcow2")

        createqcows(nombresMaquinas)
        logging.info("\n--------------Ficheros qcow creados")
        createxml(nombresMaquinas)
        logging.info("\n--------------Ficheros xml creados y modificados")
        createbridges()
        logging.info("\n--------------Bridges creados")
        definevm(nombresMaquinas)
        logging.info("\n--------------defines finished")
        createhostnames(nombresMaquinas)
        logging.info("\n--------------hostnames editados")
        createhosts(nombresMaquinas)
        logging.info("\n--------------hosts editados")
        createinterfaces(nombresMaquinas)
        logging.info("\n--------------interfaces editadas")
        editlbsysctl()
        logging.info("\n--------------lb modificado como router")
        confighost()
        logging.info("\n--------------host conectado al escenario virtual")
        logging.info("\n ---- ---- create terminado ---- ---- ")
