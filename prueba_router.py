import sys
from utils import *
import socket
import time

# debug? ==================================================
debug: bool = False
tiempo_entre_paquetes = 0 # tiempo entre el envio de cada paquete

# recibimos los parámetros desde consola =========================================
argumentos = sys.argv
if debug:
    print("argumentos:", argumentos)
headers = argumentos[1].split(',')
if debug:
   print("headers:",headers)
router_IP_destino = headers[0]
router_puerto_destino = int(headers[1])
router_ttl = int(headers[2])
direccion_origen = (argumentos[2], int(argumentos[3]))

archivo_a_enviar = "archivo.txt"

# creamos un socket que va a enviar los paquetes al router inicial para que lleguen a su origen

# socket no orientado a conexión
origen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# unimos el socket a la dirección this_address
this_adress = ("localhost", 8080)
origen.bind(this_adress)


# recibimos las lineas a enviar
# el socket no va a recibir mensajes, solo lo usaremos para enviar
# al router original los paquetes
try:
    with open(archivo_a_enviar, 'r') as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            print("linea:", linea, "\n")
            mensaje = create_final_packet(
                router_IP_destino, router_puerto_destino, router_ttl, linea+"\n")
            try:
                origen.sendto(mensaje, direccion_origen)
                time.sleep(tiempo_entre_paquetes)
            except:
                print(f"No se pudo enviar el paquete {mensaje}.\n")

except FileNotFoundError:
    print(f"El archivo {archivo_a_enviar} no se encuentra.")
