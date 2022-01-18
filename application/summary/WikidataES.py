import application.summary.Wikidata as wikidata


class WikidataES(wikidata.Wikidata):

    def __init__(self,url="http://query.wikidata.org/sparql"):
        super().__init__("es",url)        
    
