import application.summary.Wikidata as wikidata


class WikidataEN(wikidata.Wikidata):

    def __init__(self,url="http://query.wikidata.org/sparql"):
        super().__init__("en",url)        
    
