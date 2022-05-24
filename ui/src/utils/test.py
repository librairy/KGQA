import dbManager

dbDirection = "mongodb://localhost:27017"

db = dbManager.DbManager(dbDirection)

db.clearDatabase()

print(db.getCollections())