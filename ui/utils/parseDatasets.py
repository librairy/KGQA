import re
import os
import json
from tokenize import String
import pandas as pd
from pprint import pprint

#Cambiamos directorio de trabajo al directorio del script para poder abrir archivos en la misma carpeta
fileDir = os.path.dirname(os.path.realpath(__file__))
os.chdir(fileDir)

"""
Variables globales:
- keysToKeep: Campos de nuestro diccionario que querremos conservar
"""
keysToKeep = ["question","answer"]

def jsonToDict(file):
    '''
    Funcion auxiliar que dado un archivo json, lo abre y lo convierte a lista de diccionarios
    '''
    return json.loads((file.read()).decode('utf-8'))

def jsonLineToDict(file):
    '''
    Funcion auxiliar que dado un archivo json con JSONObjects en cada linea,
    lo convierte a lista de diccionarios
    '''
    return json.loads(json.dumps([json.loads(jsonLine) for jsonLine in (file.read()).decode('utf-8').splitlines()]))

def csvToDict(file):
    '''
    Funcion auxiliar que dada la ruta de un csv, lo abre y lo convierte a lista de diccionarios
    '''
    df = pd.read_csv(file, sep=";")
    #Convertimos los valores corruptos por cadenas vacias
    df = df.fillna("")
    return df.to_dict('records')

def parseDataset(file, isCsv = False, toDf = False):
    """
    Funcion que abre datasets, los formatea a nuestro gusto 
    y los devuelve como CSV o diccionario
    """
    if isCsv:
        dictList = csvToDict(file)
    else:
        try:
            dictList = jsonToDict(file)
        except:
            dictList = jsonLineToDict(file)
    for i in dictList:
        if "verbalized_answer" in i.keys():
            answer = re.search(r"\[([^\)]+)\]", i["verbalized_answer"])
            if answer:
                i["verbalized_answer"] = answer.group(1)
            i["answer"] = i.pop("verbalized_answer")    
        keysToDelete = set(i.keys()).difference(keysToKeep)
        for k in keysToDelete:
            del i[k]
    
    #Eliminamos las entradas repetidas del diccionario convirtiendo a set
    res = list({frozenset(item.items()) : item for item in dictList}.values())
    if toDf:
        return pd.DataFrame(res)
    return res