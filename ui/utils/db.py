import os
import re
import json
import certifi
import pandas as pd
from pprint import pprint
from pymongo import MongoClient

#Cambiamos directorio de trabajo al directorio del script para poder abrir archivos en la misma carpeta
fileDir = os.path.dirname(os.path.realpath(__file__))
os.chdir(fileDir)

"""
Variables globales:
- clusterName: Nombre del cluster (base de datos) en Mongo-Atlas
- userName: Nombre de usuario
- userPassword: Password del usuario
"""

clusterName = "josemvg-muheqa.awuxe.mongodb.net/JosemVG-MuHeQa"
userName = "admin"
userPassword = ""

def createConnection():
    """
    Funcion auxiliar que crea la conexion con la base de datos
    """
    ca = certifi.where()
    client = MongoClient("mongodb+srv://" + userName + ":" + userPassword + "@" + clusterName + "?retryWrites=true&w=majority", tlsCAFile = ca)
    return client.test

def importDataset(database, dataset, datasetName):
    """
    Funcion auxiliar que inserta un dataset a la base de datos
    """
    newCol = database[datasetName]
    newCol.insert_many(dataset)

def getRandomDocument(number, database, dataset):
    """
    Funcion auxiliar que devuelve un cierto numero de documentos
    aleatorios de la base de datos como lista de diccionarios
    """
    documentList = []
    randomCursor = newCol.aggregate([{ "$sample": { "size": number } }])
    for document in randomCursor:
        documentList.append(document)
    return documentList

def getStatus(database):
    """
    Funcion auxiliar que devuelve el estado del servidor de la base de datos
    """
    return database.command("serverStatus")
