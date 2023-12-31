from cola_circular import *
import re

# variables globales:
debug = False  # True para mostrar los prints de debugging
cola_de_rutas = CircularQueue()  # al inicio es vacía

# funciones de parsing  ===============================================


def create_packet(dict_packet):
    paquete = f'{dict_packet["ip"]},{dict_packet["puerto"]},{dict_packet["TTL"]},{dict_packet["mensaje"]}'
    return paquete


def parse_packet(IP_packet):
    # el paquete se recibe codificado
    separador = ","
    IP_packet = IP_packet.decode()
    IP_packet = IP_packet.rstrip("\n")
    IP_packet = IP_packet.split(separador)
    # se asume que todo lo que está desde el 3er elemento es mensaje, por si este contiene comas
    mensaje = (separador + '').join(IP_packet[3:])
    return {"ip": IP_packet[0],
            "puerto": int(IP_packet[1]),
            "TTL": int(IP_packet[2]),
            "mensaje": re.sub(r'\s+', ' ', mensaje)
            }


# tests:
IP_packet_v1 = "127.0.0.1,8881,4,hola".encode()
parsed_IP_packet = parse_packet(IP_packet_v1)
IP_packet_v2_str = create_packet(parsed_IP_packet)
IP_packet_v2 = IP_packet_v2_str.encode()
assert IP_packet_v1 == IP_packet_v2
if debug:
    print("IP_packet_v1 == IP_packet_v2 ? {}".format(
        IP_packet_v1 == IP_packet_v2))


def create_final_packet(ip, puerto, TTL, mensaje):
    dict_packet = {
        "ip": ip,
        "puerto": puerto,
        "TTL": TTL,
        "mensaje": mensaje
    }
    return create_packet(dict_packet).encode()

# funciones para trabajar los txt ===============================================


def leer_archivo(archivo_rutas):
    try:
        with open(archivo_rutas, 'r') as archivo:
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
        print(f"El archivo {archivo_rutas} no se encuentra.")
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
    if debug:
        print("cola actual:", cola_de_rutas, "\n")
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
# precaución: ejecutar este test modifica la cola de rutas global
if debug:
    archivo = "Conf_5_routers/rutas_R2_v3.txt"
    assert check_routes(archivo,
                        ("127.0.0.1", 8884)) == ("127.0.0.1", 8883)
    assert check_routes(archivo,
                        ("127.0.0.1", 8880)) == None
    assert check_routes(archivo,
                        ("127.0.0.1", 8887)) == None
