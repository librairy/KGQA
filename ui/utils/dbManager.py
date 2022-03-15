import random
import certifi
from pymongo import MongoClient

"""
Atributos de clase:
- clusterName: Nombre del cluster (base de datos) en Mongo-Atlas
- userName: Nombre de usuario
- userPassword: Password del usuario
- mongoServer: Dirección del servidor
"""
class DbManager:

    def __init__(self,serverDir, clusterName = "", userName = "", userPassword = ""):
        """
        Constructor de la clase dbManager. 
        Por defecto, el servidor Mongo sera en local y se construye con su direccion
        Si la base de datos esta en la nube (MongoDB Atlas por ej), llamar con clusterName, userName y userPassword.
        """
        self.serverDir = serverDir
        self.clusterName = clusterName
        self.userName = userName
        self.userPassword = userPassword

        if clusterName:
            self.database = MongoClient("mongodb+srv://" + userName + ":" + userPassword + "@" + clusterName + "?retryWrites=true&w=majority", tlsCAFile = certifi.where())
        else:
            self.database = MongoClient(serverDir).database

    def getCollections(self):
        """
        Funcion auxiliar que muestra las colecciones en nuestra base de datos
        """
        return self.database.list_collection_names()

    def importDataset(self, dataset, datasetName):
        """
        Funcion auxiliar que inserta un dataset a la base de datos
        """
        newCol = self.database[datasetName]
        if len(dataset) > 1:
            newCol.insert_many(dataset)
        else:
            newCol.insert_one(dataset)

    def getRandomDocument(self, number, dataset):
        """
        Funcion auxiliar que devuelve un cierto numero de documentos
        aleatorios de la base de datos como lista de diccionarios
        """
        if dataset == "All":
            dataset = random.choice(self.getCollections())

        documentList = []
        randomCursor = self.database[dataset].aggregate([{ "$sample": { "size": number } }])

        for document in randomCursor:
            documentList.append(document)
        return documentList

    def getAllDocuments(self, dataset):
        """
        Funcion auxiliar que devuelve todos los documentos de una coleccion
        como lista de diccionarios
        """
        collection = self.database[dataset]
        
        documentList = []
        for document in collection.find():
            documentList.append(document)
        
        return documentList

    def getDocumentCount(database,dataset):
        """
        Funcion auxiliar que muestra el numero de entradas en un dataset
        """
        return database[dataset].count_documents({})

    def dropCollection(self, collectionName):
        """
        Funcion auxiliar que muestra las colecciones en nuestra base de datos
        """
        if collectionName in self.getCollections():
            col = self.database[collectionName]
            col.drop()

    def clearDatabase(self):
        """
        Funcion auxiliar que vacia las colecciones de nuestra base de datos
        """
        for collectionName in self.getCollections():
            col = self.database[collectionName]
            col.drop()

    def getStatus(self):
        """
        Funcion auxiliar que devuelve el estado del servidor de la base de datos
        """
        return self.database("serverStatus")