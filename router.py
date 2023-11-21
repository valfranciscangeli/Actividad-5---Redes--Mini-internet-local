import sys
import socket
from utils import *

# debug? ==================================================
debug: bool = True

# recibimos los parámetros desde consola =========================================
argumentos: list = sys.argv
router_IP = argumentos[1]
router_puerto = int(argumentos[2])
router_rutas = argumentos[3]

# variables globales ============================================================
direccion_router_actual = (router_IP, router_puerto)
buff_size = 4096

if debug:
    print(f"direccion: {direccion_router_actual}, archivo de rutas: {router_rutas}")

# python3 router.py 127.0.0.1 8881 Conf_2_routers/rutas_R1_v1.txt
# python3 router.py 127.0.0.1 8882 Conf_2_routers/rutas_R2_v1.txt

# creacion del socket ============================================================
# socket no orientado a conexión
router = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# unimos el socket a la dirección this_address
router.bind(direccion_router_actual)

# esperamos hasta recibir un mensaje ==============================================

# vamos a recibir mensajes en un loop
while True:
    
    # aquí esperaremos hasta recibir algun mensaje
    while True:
        if debug:
            print("esperando mensaje ....")

        # recibimos el mensaje usando recvfrom
        recv_message, return_address = router.recvfrom(buff_size)

        if debug:
            print("mensaje recibido:", recv_message.decode())

        # si recibimos un mensaje saldremos de este ciclo para continuar con el código
        if recv_message != None:
            break

    paquete_ip = parse_packet(recv_message)
    destination_address = (paquete_ip["ip"], paquete_ip["puerto"])
    
    # si el mensaje es para nosotros, lo mostramos
    if destination_address == direccion_router_actual:
        print(paquete_ip["mensaje"])
    
    else:
        direccion_next_hop = check_routes(router_rutas, (paquete_ip["ip"], paquete_ip["puerto"]))

        if direccion_next_hop:
            print(f"redirigiendo paquete {paquete_ip} con destino final {destination_address} desde {direccion_router_actual} hacia {direccion_next_hop}")
            
            # hacemos forward
            fwd_message = create_packet(paquete_ip).encode()
            router.sendto(fwd_message, direccion_next_hop)
            
        else:
            print(f"No hay rutas hacia {destination_address} para paquete {paquete_ip}")