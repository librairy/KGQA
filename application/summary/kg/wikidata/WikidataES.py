import application.summary.kg.wikidata.Wikidata as wikidata


class WikidataES(wikidata.Wikidata):

    def __init__(self,url="http://query.wikidata.org/sparql",rules=True):
        super().__init__("es",url,rules)
