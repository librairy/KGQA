import application.summary.kg.dbpedia.DBpedia as dbpedia


class DBpediaEN(dbpedia.DBpedia):

    def __init__(self,url="http://dbpedia.org/sparql",rules=True):
        super().__init__("en",url,rules)
