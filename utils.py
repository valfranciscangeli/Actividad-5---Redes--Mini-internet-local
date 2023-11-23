from cola_circular import *
import re

# variables globales:
cola_de_rutas = CircularQueue()  # al inicio es vacía
debug = True

# clase para manejar paquetes ip ====================================

class PaqueteIP:
    def __init__(self, ip, puerto, ttl,mensaje=""):
        self.ip = ip
        self.puerto = puerto
        self.ttl = ttl
        self.mensaje = mensaje

    def __str__(self):
        return f'{self.ip},{self.puerto},{self.ttl},{self.mensaje}'


# funciones de parsing  ===============================================


def create_packet(paquete_ip:PaqueteIP):
    return str(paquete_ip)


def parse_packet(paquete_ip:str):
    separador = ","
    recibido = paquete_ip.decode().split(separador)
    # se asume que todo lo que está desde el 3ro elemento es mensaje, por si este contiene comas
    mensaje = (separador + '').join(recibido[3:])
    mensaje = re.sub(r'\s+', ' ', mensaje)
    return PaqueteIP(recibido[0],recibido[1], recibido[2], mensaje)




# tests:
IP_packet_v1 = "127.0.0.1,8881,4,hola".encode()
parsed_IP_packet = parse_packet(IP_packet_v1)
IP_packet_v2_str = create_packet(parsed_IP_packet)
IP_packet_v2 = IP_packet_v2_str.encode()
assert IP_packet_v1 == IP_packet_v2
if debug:
    print("IP_packet_v1 == IP_packet_v2 ? {}".format(
        IP_packet_v1 == IP_packet_v2))


# funciones para trabajar los txt ===============================================


def leer_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            lineas = archivo.readlines()
            cola_resultado = CircularQueue()
            for linea in lineas:
                linea = linea.strip().split()
                diccionario = {
                    "red": linea[0],
                    "puerto_inicial": int(linea[1]),
                    "puerto_final": int(linea[2]),
                    "ip_llegar": linea[3],
                    "puerto_llegar": int(linea[4])
                }
                cola_resultado.enqueue(diccionario)

            return cola_resultado

    except FileNotFoundError:
        if debug:
            print(f"El archivo {nombre_archivo} no se encuentra.")
        return None


# test
nombre_del_archivo = 'Conf_5_routers/rutas_R2_v3.txt'
resultado = leer_archivo(nombre_del_archivo)

if resultado and debug:
    print(resultado)


# manejo de rutas ==============================================

def check_routes(routes_file_name, destination_address):
    global cola_de_rutas
    if cola_de_rutas.is_empty():
        cola_de_rutas = leer_archivo(routes_file_name)
    print("cola actual:", cola_de_rutas, "\n") #mostramos la cola de rutas
    dest_ip = destination_address[0]
    dest_port = destination_address[1]

    # buscamos la ruta en la lista
    total_rutas = len(cola_de_rutas.queue)
    contador = 0
    while contador < total_rutas:
        primera = cola_de_rutas.get_first()
        red = primera["red"]
        pto_ini = primera["puerto_inicial"]
        pto_fin = primera["puerto_final"]
        if dest_ip == red and pto_ini <= dest_port <= pto_fin:
            # encontramos la ruta buscada
            return (primera["ip_llegar"], primera["puerto_llegar"])

        contador += 1

    # no se encontró una ruta
    return None


# test:
# archivo = "Conf_5_routers/rutas_R2_v3.txt"
# assert check_routes(archivo,
#                     ("127.0.0.1", 8884)) == ("127.0.0.1", 8883)
# assert check_routes(archivo,
#                     ("127.0.0.1", 8880)) == None
# assert check_routes(archivo,
#                     ("127.0.0.1", 8887)) == None
