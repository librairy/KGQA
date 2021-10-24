import spacy
import requests

import application.kg.Summarizer as kg_summarizer


class Wikidata(kg_summarizer.Summarizer):

    def __init__(self,lang,url):
        super().__init__(lang)
        self.wikidata_url = url
        self.lang = lang
        
        print("Loading Wikidata Entity Linker ("+lang+") from spaCy model")

        if lang == "en":
            self.nlp = spacy.load("en_core_web_lg")
        else:
           self.nlp = spacy.blank(lang) 
        self.nlp.add_pipe('sentencizer')
        # add pipeline (declared through entry_points in setup.py)
        self.nlp.add_pipe("entityLinker", last=True)
    

    def get_summary(self,question):
        doc = self.nlp(question)
        
        text = ""
        
        for entity in doc._.linkedEntities:
            properties = {}
            print("Entity:",entity)
            
            fromRelations = self.get_from_properties(entity.get_id())
            
            if fromRelations != None:
                for result in fromRelations["results"]["bindings"]:
                    properties[result["propertyLabel"]["value"]]= result["value"]["value"]
            
            toRelations = self.get_to_properties(entity.get_id())
            
            if toRelations != None:
                for result in toRelations["results"]["bindings"]:
                    properties[result["propertyLabel"]["value"]]= result["value"]["value"]
        
            partial_summary = super().get_single_fact_summary(entity.get_label(),properties)
            text +=  partial_summary
        return text
    

    def get_from_properties(self,entity):
        print("Entity:", entity)
        query = """SELECT ?propertyLabel
                    (GROUP_CONCAT(DISTINCT ?valueLabel;separator=", ") AS ?value)
                WHERE{
                    ?item ?label \" """+entity+" \"@"+self.lang+""" .
                    ?item ?prop ?value .
                    ?property wikibase:directClaim ?prop .
                    SERVICE wikibase:label {bd:serviceParam wikibase:language """+self.lang+""".
                                        ?property rdfs:label ?propertyLabel .
                                        ?value rdfs:label ?valueLabel .}
            }
            GROUP BY ?propertyLabel
        """
        payload = {
        	#'default-graph-uri': 'http://wikidata.org', 
        	'query': query, 
        	'format': 'application/json', 
        	'timeout': 120000, 
        	'signal_void':'on', 
        	'signal_unconnected':'on' }
        response = requests.get(self.wikidata_url, params=payload)
    	
        return response.json()


    def get_to_properties(self,entity):
    
    	query = """"SELECT ?propertyLabel
                    (GROUP_CONCAT(DISTINCT ?valueLabel;separator=", ") AS ?value)
                WHERE{
                    ?item ?label \" """+entity+" \"@"+self.lang+""" .
                    ?item ?prop ?value .
                    ?property wikibase:directClaim ?prop .
                    SERVICE wikibase:label {bd:serviceParam wikibase:language """+self.lang+""".
                                        ?property rdfs:label ?propertyLabel .
                                        ?value rdfs:label ?valueLabel .}
            }
            GROUP BY ?propertyLabel
        """
    
    	payload = {
        	#'default-graph-uri': 'http://wikidata.org', 
        	'query': query, 
        	'format': 'application/json', 
        	'timeout': 120000, 
        	'signal_void':'on', 
        	'signal_unconnected':'on' }
    
    	response = requests.get(self.wikidata_url, params=payload)
    
    	return response.json()

