from logging.handlers import RotatingFileHandler

import application.summary.DBpediaEN as dbpedia_en
import application.summary.DBpediaES as dbpedia_es
import application.summary.WikidataEN as wikidata_en
import application.summary.WikidataES as wikidata_es


dbpediaEN = dbpedia_en.DBpediaEN("http://localhost:8890/sparql")
dbpediaES = dbpedia_es.DBpediaES()
wikidataEN = wikidata_en.WikidataEN()
wikidataES = wikidata_es.WikidataES()


query = "Where was Fernando Alonso born?"
print(query)
summary = dbpediaEN.get_summary(query)
print(summary)