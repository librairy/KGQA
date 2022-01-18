import application.summary.DBpedia as dbpedia


class DBpediaES(dbpedia.DBpedia):

    def __init__(self,url="https://es.dbpedia.org/sparql"):
        super().__init__("es",url)
    
    
