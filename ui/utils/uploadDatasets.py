import db
import glob
import parseDatasets

#Creamos la conexion a la base de datos
database = db.createConnection()

#Ejecutamos parseDataset para nuestros datasets (json y csv)
datasetFiles = glob.glob("*.json")
[db.importDataset(database, parseDataset(i), i.split(".")[0].lower()) for i in datasetFiles if i != "credentials.json"]

datasetFiles = glob.glob("*.csv")
for i in datasetFiles:
    db.importDataset(database, parseDataset(i, isCsv=True), i.split(".")[0].lower())

#Vemos que documentos hay en la base de datos
db.getCollections(database)