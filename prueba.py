import os
#os.system('python3 router.py 127.0.0.1 8882 Conf_2_routers/rutas_R2_v1.txt')

import subprocess


# Comando para ejecutar el archivo en una nueva terminal
comando = "python3 router.py 127.0.0.1 8882 Conf_2_routers/rutas_R2_v1.txt"

for i in range(1,4):
    comando = f"x-terminal-emulator -e 'python3 router.py 127.0.0.1 888{i} Conf_2_routers/rutas_R{i}_v1.txt'"
    comando = f"python3 router.py 127.0.0.1 888{i} Conf_2_routers/rutas_R{i}_v1.txt"

    # Utiliza subprocess para ejecutar el comando en una nueva terminal
    subprocess.Popen(comando, shell=True)
