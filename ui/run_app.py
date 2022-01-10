import os
import time
import requests
import subprocess
from multiprocessing import Process

def runServer(dir):
    """
    Funcion auxiliar que ejecuta el servidor de EQA
    """
    p = subprocess.Popen(["python", "manage.py", "runserver"], cwd = dir)        

def checkEQAServer():
    """
    Funcion auxiliar que comprueba que el servidor de EQA esta corriendo
    """
    files = {
        'question': (None, "Where was Fernando Alonso born?"),
    }

    while True:
        try:
            requests.get("http://127.0.0.1:5000/eqakg/dbpedia/en?text=false", files = files)
            break
        except requests.exceptions.ConnectionError:
            print("EQA SERVER CHECK > Failed to establish connection")
            time.sleep(30)

#Obtenemos el directorio padre y el directorio del archivo
fileDir = os.path.dirname(os.path.realpath(__file__))
parentDir = os.path.dirname(fileDir)

if __name__ == '__main__':

    #Corremos el servidor de EQA en otro hilo
    p = Process(target = runServer, args = (parentDir, ))
    p.start()

    #Comprobamos que el servidor de EQA se este ejecutando
    checkEQAServer()

    #Corremos la interfaz web
    p = subprocess.run(["streamlit", "run", "webapp.py"], cwd = fileDir)    