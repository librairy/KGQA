import spacy
import requests

import application.summary.Summarizer as kg_summarizer


class DBpedia(kg_summarizer.Summarizer):

    def __init__(self,lang,url):
        super().__init__(lang)
        self.dbpedia_url = url
        self.lang = lang
        print("Linked to DBpedia("+lang+"):",self.dbpedia_url)
        #nlp = spacy.load("en_core_web_lg")
        self.nlp = spacy.blank(lang)
        self.nlp.add_pipe('dbpedia_spotlight', config={'confidence': 0.4, 'overwrite_ents':False})


    def get_summary(self,question):
        doc = self.nlp(question)
        entities = [{ 'id': e.kb_id_, 'name': e.text} for e in doc.spans['dbpedia_spotlight']]
        text = self.get_summary_from_entities(question, entities)
        return text


    def get_summary_from_entities(self,question,entities):
        text = ""
        print("DBpedia entities:",entities)
        for entity in entities:
            properties = {}

            fromRelations = self.get_from_properties(entity['id'])

            if fromRelations != None:
                for result in fromRelations["results"]["bindings"]:
                    properties[result["propertyLabel"]["value"]]= result["valueLabel"]["value"]

            toRelations = self.get_to_properties(entity['id'])

            if toRelations != None:
                for result in toRelations["results"]["bindings"]:
                    properties[result["propertyLabel"]["value"]]= result["valueLabel"]["value"]

            partial_summary = super().get_single_fact_summary(entity['name'],properties)
            text +=  partial_summary
        return text

    def get_from_properties(self,entity):
        query = "PREFIX dbr: <http://dbpedia.org/resource/> \n" + "SELECT ?propertyLabel (GROUP_CONCAT(DISTINCT ?valueLabel ; SEPARATOR=\", \") AS ?valueLabel ) {\n"+ "<" + entity + """> ?property ?value .
        	OPTIONAL {?property rdfs:comment ?auxProperty .}
        	FILTER (!bound(?auxProperty ) || !strstarts(str(?auxProperty),
        					str("Reserved for DBpedia")))

        	FILTER (!strstarts( str(?property),
        					str("http://dbpedia.org/ontology/abstract")))

        	?property rdfs:label ?propertyLabel .
        	FILTER (LANGMATCHES(LANG(?propertyLabel ), \""""+self.lang+"""\"))

        	OPTIONAL {?value rdfs:label ?auxValue .}
        	BIND (IF(isLiteral(?value), ?value, ?auxValue) AS ?valueLabel)
        	FILTER (isNumeric(?valueLabel) ||
        					LANGMATCHES(LANG(?valueLabel ), \""""+self.lang+"""\"))
        }
        """

        payload = {
        	#'default-graph-uri': 'http://dbpedia.org',
        	'query': query,
        	'format': 'application/json',
        	'timeout': 120000,
        	'signal_void':'on',
        	'signal_unconnected':'on'
        }

        try:
            response = requests.get(self.dbpedia_url, params=payload)
            return response.json()
        except Exception as e:
            print("Error on DBpedia query:",e)
        return {}


    def get_to_properties(self,entity):

        query = "PREFIX dbr: <http://dbpedia.org/resource/> \n" + "SELECT ?propertyLabel (GROUP_CONCAT(DISTINCT ?valueLabel ; SEPARATOR=\", \") AS ?valueLabel ) { \n" + "?value ?property  <" + entity + """>.

        	OPTIONAL {?property rdfs:comment ?auxProperty .}
        	FILTER (!bound(?auxProperty ) || !strstarts(str(?auxProperty),
                        	str("Reserved for DBpedia")))

        	FILTER (!strstarts( str(?property),
                        	str("http://dbpedia.org/ontology/abstract")))

        	?property rdfs:label ?propertyLabel .
        	FILTER (LANGMATCHES(LANG(?propertyLabel ), \""""+self.lang+"""\"))

        	OPTIONAL {?value rdfs:label ?auxValue .}
        	BIND (IF(isLiteral(?value), ?value, ?auxValue) AS ?valueLabel)
        	FILTER (isNumeric(?valueLabel) ||
                        	LANGMATCHES(LANG(?valueLabel ), \""""+self.lang+"""\"))
        }
        """

        payload = {
        	#'default-graph-uri': 'http://dbpedia.org',
        	'query': query,
        	'format': 'application/json',
        	'timeout': 120000,
        	'signal_void':'on',
            'signal_unconnected':'on'
        }

        try:
            response = requests.get(self.dbpedia_url, params=payload)
            return response.json()
        except Exception as e:
            print("Error on DBpedia query:",e)
        return {}
