import os
import random
import certifi
from pymongo import MongoClient

#Cambiamos directorio de trabajo al directorio del script para poder abrir archivos en la misma carpeta
fileDir = os.path.dirname(os.path.realpath(__file__))
os.chdir(fileDir)

"""
Variables globales:
- clusterName: Nombre del cluster (base de datos) en Mongo-Atlas
- userName: Nombre de usuario
- userPassword: Password del usuario
- mongoServer: Dirección del servidor
"""

clusterName = "josemvg-muheqa.awuxe.mongodb.net/JosemVG-MuHeQa"
userName = "admin"
userPassword = ""
serverDir = "mongodb://localhost:27017"

def createConnection(cloud = False):
    """
    Funcion auxiliar que crea la conexion con la base de datos
    Si la base de datos esta en la nube (MongoDB Atlas), llamar con cloud = True
    Por defecto, el metodo se ejecuta con parametro cloud = False
    """
    ca = certifi.where()
    if cloud:
        client = MongoClient("mongodb+srv://" + userName + ":" + userPassword + "@" + clusterName + "?retryWrites=true&w=majority", tlsCAFile = ca)
    else:
        client = MongoClient(host = serverDir)
    return client.test

def importDataset(database, dataset, datasetName):
    """
    Funcion auxiliar que inserta un dataset a la base de datos
    """
    newCol = database[datasetName]
    if len(dataset) > 1:
        newCol.insert_many(dataset)
    else:
        newCol.inser_one(dataset)

def getRandomDocument(number, database, dataset):
    """
    Funcion auxiliar que devuelve un cierto numero de documentos
    aleatorios de la base de datos como lista de diccionarios
    """
    if dataset == "All":
        dataset = random.choice(getCollections(database))

    documentList = []
    randomCursor = database[dataset].aggregate([{ "$sample": { "size": number } }])

    for document in randomCursor:
        documentList.append(document)
    return documentList

def getCollections(database):
    """
    Funcion auxiliar que muestra las colecciones en nuestra base de datos
    """
    return database.list_collection_names()


def getDocumentCount(database,dataset):
    """
    Funcion auxiliar que muestra el numero de entradas en un dataset
    """
    return database[dataset].count_documents({})

def dropCollection(database, collectionName):
    """
    Funcion auxiliar que muestra las colecciones en nuestra base de datos
    """
    if collectionName in getCollections(database):
        col = database[collectionName]
        col.drop()

def clearDatabase(database):
    """
    Funcion auxiliar que vacia las colecciones de nuestra base de datos
    """
    for collectionName in getCollections(database):
        col = database[collectionName]
        col.drop()

def getStatus(database):
    """
    Funcion auxiliar que devuelve el estado del servidor de la base de datos
    """
    return database.command("serverStatus")