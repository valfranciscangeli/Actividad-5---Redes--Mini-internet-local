import sys
from utils import *

# debug? ==================================================
debug: bool = True

# recibimos los parámetros desde consola =========================================
##  python3 prueba_router.py 127.0.0.1,8885,10 127.0.0.1 8881
argumentos: list = sys.argv
headers = argumentos[1].split()
router_IP_destino = headers[0]
router_puerto_destino = int(headers[1])
router_ttl = int(headers[2])
router_IP_origen = argumentos[2]
router_puerto_origen = int(argumentos[3])

# creamos un socket que va a enviar los paquetes al router inicial para que lleguen a su origen


# recibimos las lineas a enviar

