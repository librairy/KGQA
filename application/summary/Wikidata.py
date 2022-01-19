import spacy
import requests

import application.summary.Summarizer as kg_summarizer


class Wikidata(kg_summarizer.Summarizer):

    def __init__(self,lang,url):
        super().__init__(lang)
        self.wikidata_url = url
        self.lang = lang

        print("Linked to Wikidata ("+lang+"):",self.wikidata_url)

        self.nlp = spacy.load("en_core_web_sm")
        #self.nlp = spacy.blank(lang)
        self.nlp.add_pipe('sentencizer')
        # add pipeline (declared through entry_points in setup.py)
        self.nlp.add_pipe("entityLinker", last=True)


    def get_summary(self,question):
        doc = self.nlp(question)
        entities = [{ 'id':"Q"+str(e.get_id()), 'name':e.get_label() } for e in doc._.linkedEntities]
        return self.get_summary_from_entities(question, entities)

    def get_summary_from_entities(self,question,entities):
        text = ""
        print("Wikidata Entities:",entities)
        for entity in entities:
            properties = {}

            fromRelations = self.get_from_properties(entity['id'])

            if fromRelations != None and 'results' in fromRelations :
                for result in fromRelations["results"]["bindings"]:
                    properties[result["propertyLabel"]["value"]]= result["value"]["value"]

            toRelations = self.get_to_properties(entity['id'])

            if toRelations != None and 'results' in toRelations:
                for result in toRelations["results"]["bindings"]:
                    properties[result["propertyLabel"]["value"]]= result["value"]["value"]

            partial_summary = super().get_single_fact_summary(entity['name'],properties)
            text +=  partial_summary
        return text

    def get_from_properties(self,entity):
        entity_uri = "wd:" + str(entity)
        query = """SELECT ?propertyLabel
                    (GROUP_CONCAT(DISTINCT ?valueLabel;separator=", ") AS ?value)
                WHERE{
                    """+entity_uri+""" ?prop ?value .
                    ?property wikibase:directClaim ?prop .
                    SERVICE wikibase:label {bd:serviceParam wikibase:language \""""+self.lang+"""\" .
                                        ?property rdfs:label ?propertyLabel .
                                        ?value rdfs:label ?valueLabel .}
            }
            GROUP BY ?propertyLabel
        """

        payload = {
        	#'default-graph-uri': 'http://wikidata.org',
        	'query': query,
        	'format': 'json',
        	'timeout': 120000,
        	'signal_void':'on',
        	'signal_unconnected':'on' }
        try:
            response = requests.get(self.wikidata_url, params=payload)
            return response.json()
        except Exception as e:
            print("Error on Wikidata query:",e)
            return {}


    def get_to_properties(self,entity):
        entity_uri = "wd:" + str(entity)
        query = """SELECT ?propertyLabel
                    (GROUP_CONCAT(DISTINCT ?valueLabel;separator=", ") AS ?value)
                WHERE{
                    ?value ?prop """+entity_uri+""" .
                    ?property wikibase:directClaim ?prop .
                    SERVICE wikibase:label {bd:serviceParam wikibase:language \""""+self.lang+"""\" .
                                        ?property rdfs:label ?propertyLabel .
                                        ?value rdfs:label ?valueLabel .}
            }
            GROUP BY ?propertyLabel
        """

        payload = {
        	#'default-graph-uri': 'http://wikidata.org',
        	'query': query,
        	'format': 'json',
        	'timeout': 120000,
        	'signal_void':'on',
        	'signal_unconnected':'on' }

        try:
            response = requests.get(self.wikidata_url, params=payload)
            return response.json()
        except Exception as e:
            print("Error on Wikidata query:",e)
            return {}
