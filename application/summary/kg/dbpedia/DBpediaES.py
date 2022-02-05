import application.summary.kg.dbpedia.DBpedia as dbpedia


class DBpediaES(dbpedia.DBpedia):

    def __init__(self,url="https://es.dbpedia.org/sparql",rules=True):
        super().__init__("es",url,rules)
