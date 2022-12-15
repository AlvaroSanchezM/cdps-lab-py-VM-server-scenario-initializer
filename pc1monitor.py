import os
import logging
import json

def monitoriza():	#Saca una "foto" instantánea del estado de las máquinas virtuales
	logging.debug("Monitoriza llamado 1 vez")
	os.system("sudo virsh list --all")

def monitorizaPers():		#Saca el estado de las máquinas virtuales en una ventana aparte, de forma continua
        logging.debug("Monitoriza persistente en una ventana nueva")
        logging.info("Se monitoriza el estado de cada máquina en otra ventana")
        #os.system("gnome-terminal -x sh -c \"watch sudo virsh list --all; bash\"")
        os.system("xterm -e 'watch -n 0,5 sudo virsh list --all'&")
        os.system("sleep 1")
        os.system("^C")

#def monitorPersistenteAparte():
#	#crear archivo de control
#	ctlfile = open('monitorPers.txt', 'w')
#	ctlfile.close()
#	os.system("watch sudo virsh list --all")
#	while os.path.isfile("monitorPers.txt"):
#		os.system("sleep 2")
#	os.system("^C")#Cierra la ventana aparte pero saca error en ventana local
	
	
	
	
	
	
