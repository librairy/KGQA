import application.summary.DBpedia as dbpedia


class DBpediaEN(dbpedia.DBpedia):

    def __init__(self,url="http://dbpedia.org/sparql"):
        super().__init__("en",url)        
    

