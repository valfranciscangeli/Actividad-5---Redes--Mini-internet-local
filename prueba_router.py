import sys
from utils import *
import socket

# debug? ==================================================
debug: bool = True

# recibimos los parámetros desde consola =========================================
# python3 prueba_router.py 127.0.0.1,8885,10 127.0.0.1 8881
argumentos: list = sys.argv
headers = argumentos[1].split()
router_IP_destino = headers[0]
router_puerto_destino = int(headers[1])
router_ttl = int(headers[2])
router_IP_origen = argumentos[2]
router_puerto_origen = int(argumentos[3])

# creamos un socket que va a enviar los paquetes al router inicial para que lleguen a su origen
# socket no orientado a conexión
origen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# unimos el socket a la dirección this_address
this_adress = (router_IP_origen, 8080)
origen.bind(this_adress)

# recibimos las lineas a enviar
# el socket no va a recibir mensajes, solo lo usaremos para enviar
direccion_origen = (router_IP_origen, router_puerto_origen)
archivo_a_enviar = "archivo.txt"
try:
    with open(archivo_a_enviar, 'r') as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            mensaje = create_final_packet(
                router_IP_destino, router_puerto_destino, router_ttl, linea+"\n")
            try:
                origen.sendto(mensaje, direccion_origen)
            except:
                print(f"No se pudo enviar el paquete {mensaje}.")

except FileNotFoundError:
    print(f"El archivo {archivo_a_enviar} no se encuentra.")
