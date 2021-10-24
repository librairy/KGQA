import spacy
import requests

import application.kg.Summarizer as kg_summarizer
import application.kg.DBpedia as dbpedia


class DBpediaEN(dbpedia.DBpedia):

    def __init__(self):
        super().__init__("en","http://dbpedia.org/sparql")
        print("Ready to answer question from the English edition of DBpedia")
    

