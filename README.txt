# Authors:
# alvaro.sanchezm@alumnos.upm.es
# e.gdealfonso@alumnos.upm.es

Para ejecutar este script, el archivo "gestiona-pc1" necesita permisos de ejecución.
Estos se pueden garantizar mediante el comando "chmod +x gestiona-pc1".

VERSIÓN: V6

Modo de empleo: /gestiona-pc1. <orden> [OPCIÓN]

<orden> posibles:
 create  : crea los ficheros .qcow2 de diferencias, y los de especificación en XML,
           de cada MV, así como los bridges virtuales que soportan las LAN del escenario.
    [NÚMERO] : número de servidores web que se crean (entre 1 y 5).
                Sin NÚMERO, se toman 2 por defecto.

 start   : arranca las máquinas virtuales y crea su consola

 stop    : para (detiene) las máquinas virtuales (sin liberarlas)

 destroy : libera el escenario, borrando todos los ficheros creados

 monitor : muestra el estado de las máquinas.
    [-pers] : con esta opción incluida en el comando, el estado de las máquinas
               se abre en una ventana nueva
    
 --help  : para ver este texto de ayuda


-Versión 6
Cambios comparado con V5:
-La ventana abierta con "monitor -pers" se cierra cuando se ejecuta la orden "create".
-Mayor uso de la librería logging. Por defecto el programa saca solamente trazas, las respuestas automáticas de cada comando y los avisos de error.
-Para sacar trazas extras, hace falta incluir un archivo gestiona-pc1.json con el valor "debug": true, si aún no existe, y si existe, introducir el valor anterior en el fichero.

-Versión 5
Acciones urgentes V5:
-Cerrar la ventana abierta con "monitor -pers" cuando se ejecuta la <orden> "destroy"
+Solucionado
Cambios comparado con V4:
-Añadida <orden> "monitor", que muestra el estado instantáneo de las máquinas.
-Añadida en "monitor" [OPCIÓN] "-pers" que muestra en una ventana de xterm nueva, el estado de las máquinas actualizado cada 2 segundos.
		Esta ventana hay que cerrarla manualmente, No se cierra cuando se ejecuta la <orden> "destroy".
-Modificado el código interno de pc1create.py en createinterfaces() para que el bucle for sea más compacto.
