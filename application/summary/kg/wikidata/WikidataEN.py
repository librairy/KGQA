import application.summary.kg.wikidata.Wikidata as wikidata


class WikidataEN(wikidata.Wikidata):

    def __init__(self,url="http://query.wikidata.org/sparql",rules=True):
        super().__init__("en",url,rules)
