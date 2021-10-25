import application.summary.Wikidata as wikidata


class WikidataEN(wikidata.Wikidata):

    def __init__(self):
        super().__init__("en","https://query.wikidata.org/sparql")
        print("Ready to answer question from the English edition of Wikidata")
    
