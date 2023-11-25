import sys
import socket
from utils import *

# debug? ==================================================
debug: bool = True  # True para mostrar mensajes de debuggeo

# recibimos los parámetros desde consola =========================================
argumentos: list = sys.argv
router_IP = argumentos[1]
router_puerto = int(argumentos[2])
router_rutas = argumentos[3]

# variables globales ============================================================
direccion_router_actual = (router_IP, router_puerto)
buff_size = 4096

if debug:
    print(
        f"direccion: {direccion_router_actual}, archivo de rutas: {router_rutas}")


# creacion del socket ============================================================
# socket no orientado a conexión
router = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# unimos el socket a la dirección direccion_router_actual
router.bind(direccion_router_actual)

# esperamos hasta recibir un mensaje ==============================================

# vamos a recibir mensajes en un loop
while True:

    # aquí esperaremos hasta recibir algun mensaje
    while True:
        if debug:
            print("===================== \nesperando mensaje .... \n")

        # recibimos el mensaje usando recvfrom
        recv_message, return_address = router.recvfrom(buff_size)

        if debug:
            print("mensaje recibido:", recv_message.decode(), "\n")

        # si recibimos un mensaje saldremos de este ciclo para continuar con el código
        if recv_message != None:
            break

    paquete_ip = parse_packet(recv_message)
    destination_address = (paquete_ip["ip"], paquete_ip["puerto"])
    ttl = paquete_ip["TTL"]

    if ttl > 0:  # agregamos condicion de que tenga vida para procesarlo
        # si el mensaje es para nosotros, lo mostramos
        if destination_address == direccion_router_actual:
            print(paquete_ip["mensaje"])
        # debemos reenviar el paquete
        else:
            # buscamos una direccion para reenviar
            direccion_next_hop = check_routes(
                router_rutas, (paquete_ip["ip"], paquete_ip["puerto"]))

            # revisamos si encontramos ruta de reenvio
            if direccion_next_hop:
                # vamos a disminuir el ttl antes de mandar
                paquete_ip["TTL"] -= 1

                # avisamos que se va a mandar
                print(
                    f"redirigiendo paquete {paquete_ip} con destino final {destination_address} desde {direccion_router_actual} hacia {direccion_next_hop}\n")

                # hacemos forward
                fwd_message = create_packet(paquete_ip).encode()
                router.sendto(fwd_message, direccion_next_hop)

            else:
                print(
                    f"No hay rutas hacia {destination_address} para paquete {paquete_ip}\n")
    else:
        print(f"Se recibió paquete {paquete_ip} con TTL 0")
