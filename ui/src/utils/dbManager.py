import random
import certifi
from pymongo import MongoClient

class DbManager:

    def __init__(self,serverDir, clusterName = "", userName = "", userPassword = ""):
        """
        Class constructor
        """
        self.serverDir = serverDir
        self.clusterName = clusterName
        self.userName = userName
        self.userPassword = userPassword

        if clusterName and userName and userPassword:
            self.database = MongoClient("mongodb+srv://" + userName + ":" + userPassword + "@" + clusterName + "?retryWrites=true&w=majority", tlsCAFile = certifi.where())
        else:
            self.database = MongoClient(serverDir).database

    def getCollections(self):
        """
        Method that returns the name of the collections in the database
        """
        return self.database.list_collection_names()

    def importDataset(self, dataset, datasetName):
        """
        Method that imports a dataset into the database
        """
        newCol = self.database[datasetName]
        if len(dataset) > 1:
            newCol.insert_many(dataset)
        else:
            newCol.insert_one(dataset)

    def getRandomDocument(self, number, dataset):
        """
        Method that returns number random documents from a dataset
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
        Method that returns all documents from a dataset
        """
        collection = self.database[dataset]
        
        documentList = []
        for document in collection.find():
            documentList.append(document)
        
        return documentList

    def getDocumentCount(database,dataset):
        """
        Method that returns the number of documents in a dataset
        """
        return database[dataset].count_documents({})

    def dropCollection(self, collectionName):
        """
        Method that drops a collection
        """
        if collectionName in self.getCollections():
            col = self.database[collectionName]
            col.drop()

    def clearDatabase(self):
        """
        Method that clears the database
        """
        for collectionName in self.getCollections():
            col = self.database[collectionName]
            col.drop()

    def getStatus(self):
        """
        Method that returns the status of the database
        """
        return self.database("serverStatus")