import application.kg.DBpedia as dbpedia


class DBpediaES(dbpedia.DBpedia):

    def __init__(self):
        super().__init__("es","https://es.dbpedia.org/sparql/")
        print("Ready to answer question from the Spanish edition of DBpedia")
    
