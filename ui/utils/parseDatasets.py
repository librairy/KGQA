import re
import os
import glob
import json
import pandas as pd
from pprint import pprint
import db

#Cambiamos directorio de trabajo al directorio del script para poder abrir archivos en la misma carpeta
fileDir = os.path.dirname(os.path.realpath(__file__))
os.chdir(fileDir)

"""
Variables globales:
- keysToKeep: Campos de nuestro diccionario que querremos conservar
"""
keysToKeep = ["question","answer"]

def jsonToDict(route):
    '''
    Funcion auxiliar que dada la ruta de un json, lo abre y lo convierte a lista de diccionarios
    '''
    with open(route, encoding="utf-8") as f:
        return json.load(f)

def jsonLineToDict(JSONRoute):
    '''
    Funcion auxiliar que dado un archivo json con JSONObjects en cada linea,
    lo abre y lo convierte a lista de diccionarios
    '''  
    with open(JSONRoute) as f:
        jsonList = list(f)
    
    return json.loads(json.dumps([json.loads(jsonLine) for jsonLine in jsonList]))

def csvToDict(route):
    '''
    Funcion auxiliar que dada la ruta de un csv, lo abre y lo convierte a lista de diccionarios
    '''
    df = pd.read_csv(route, sep=";")
    #Convertimos los valores corruptos por cadenas vacias
    df = df.fillna("")
    return df.to_dict('records')

def parseDataset(route, isCsv = False, toDf = False):
    """
    Funcion que abre datasets, los formatea a nuestro gusto 
    y los devuelve como CSV o diccionario
    """
    if isCsv:
        dictList = csvToDict(route)
    else:
        try:
            dictList = jsonToDict(route)
        except:
            dictList = jsonLineToDict(route)
    
    for i in dictList:
        if "verbalized_answer" in i.keys():
            answer = re.search(r"\[([^\)]+)\]", i["verbalized_answer"])
            if answer:
                i["verbalized_answer"] = answer.group(1)
            i["answer"] = i.pop("verbalized_answer")    
        keysToDelete = set(i.keys()).difference(keysToKeep)
        for k in keysToDelete:
            del i[k]
    
    if toDf:
        return pd.DataFrame(dictList)   
    return dictList

#Creamos la conexion a la base de datos
database = db.createConnection()

#db.getCollections(database)

#db.dropCollection(database,"vanilla")

#Ejecutamos parseDataset para nuestros datasets
jsonFiles = glob.glob("*.json")
for i in jsonFiles:
    db.importDataset(database, parseDataset(i), i.split(".")[0].lower())

csvFiles = glob.glob("*.csv")
for i in csvFiles:
    db.importDataset(database, parseDataset(i, isCsv=True), i.split(".")[0].lower())