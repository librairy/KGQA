import application.summary.Wikidata as wikidata


class WikidataES(wikidata.Wikidata):

    def __init__(self):
        super().__init__("es","http://query.wikidata.org/sparql")
        print("Ready to answer question from the Spanish edition of Wikidata")
    
