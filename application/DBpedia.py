# Author: Rafael Ines Guillen
# Project: Explainable QA over KG
# File: DBèdia.py
# Purpose: solve questions to DBpedia in english


# Loading libraries and dependencies

import spacy

from transformers import AutoTokenizer, TFAutoModelForQuestionAnswering
import tensorflow as tf
import requests

# Loading libraries and dependencies

dbpedia_url = "http://dbpedia.org/sparql"

print("Loading SpaCy model: en_core_web_lg")
#print("Loading SpaCy model: blank")
#nlp = spacy.load("en_core_web_lg")
nlp = spacy.blank('en')
nlp.add_pipe('dbpedia_spotlight', config={'confidence': 0.4, 'overwrite_ents':False})
print("Loaded")

print("Loding BERT model: bert-large-uncased-whole-word-masking-finetuned-squad")
tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
model = TFAutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
print("Loaded")
print("Ready to answer question from DBpedia in english:")


# Question treatment

def DBpedia(question):	
	print(question)

	doc = nlp(question)
	
	text = documentRetrieval(doc)

	return bertAnswer(question, text)


# Document retrieval

def documentRetrieval(doc):

	text = ""

	for ent in doc.spans['dbpedia_spotlight']:
		results = relationFromEntity(ent.kb_id_)
		text = text + query2Text(ent.text, results)
		
		# Second direction
		text = text + '\n'+ '\n'

		results = relationToEntity(ent.kb_id_)
		text = text + query2Text(ent.text,results)

		return text


# BERT QA

def bertAnswer(question, text):

	inputs = tokenizer(question, text, add_special_tokens=True, return_tensors="tf",truncation=True)

	input_ids = inputs["input_ids"].numpy()[0]
	   
	outputs = model(inputs)
	answer_start_scores = outputs.start_logits
	answer_end_scores = outputs.end_logits
	 
	answer_start = tf.argmax(
	    answer_start_scores, axis=1
	).numpy()[0]  # Get the most likely beginning of answer with the argmax of the score
	answer_end = (
	    tf.argmax(answer_end_scores, axis=1) + 1
	).numpy()[0]  # Get the most likely end of answer with the argmax of the score
	answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

	print(f"Question: {question}")
	print(f"Answer: {answer}")

	return [answer,text]


# Query part

## Relation from the entity

def relationFromEntity(entity):
	query = "PREFIX dbr: <http://dbpedia.org/resource/> \n" + "SELECT ?propertyLabel (GROUP_CONCAT(DISTINCT ?valueLabel ; SEPARATOR=\", \") AS ?valueLabel ) {\n"+ "<" + entity + """> ?property ?value .
		OPTIONAL {?property rdfs:comment ?auxProperty .}
		FILTER (!bound(?auxProperty ) || !strstarts(str(?auxProperty),
						str("Reserved for DBpedia")))

		FILTER (!strstarts( str(?property),
						str("http://dbpedia.org/ontology/abstract")))

		?property rdfs:label ?propertyLabel .
		FILTER (LANGMATCHES(LANG(?propertyLabel ), "en"))

		OPTIONAL {?value rdfs:label ?auxValue .}
		BIND (IF(isLiteral(?value), ?value, ?auxValue) AS ?valueLabel)
		FILTER (isNumeric(?valueLabel) || 
						LANGMATCHES(LANG(?valueLabel ), "en"))
	}
	"""

	payload = {
    	'default-graph-uri': 'http://dbpedia.org', 
    	'query': query, 
    	'format': 'application/json', 
    	'timeout': 120000, 
    	'signal_void':'on', 
    	'signal_unconnected':'on' }

	response = requests.get(dbpedia_url, params=payload)
	
	return response.json()


## Relation to the entity

def relationToEntity(entity):

	query = "PREFIX dbr: <http://dbpedia.org/resource/> \n" + "SELECT ?propertyLabel (GROUP_CONCAT(DISTINCT ?valueLabel ; SEPARATOR=\", \") AS ?valueLabel ) { \n" + "?value ?property  <" + entity + """>.
    
		OPTIONAL {?property rdfs:comment ?auxProperty .}
    	FILTER (!bound(?auxProperty ) || !strstarts(str(?auxProperty),
                    	str("Reserved for DBpedia")))

    	FILTER (!strstarts( str(?property),
                    	str("http://dbpedia.org/ontology/abstract")))

    	?property rdfs:label ?propertyLabel .
    	FILTER (LANGMATCHES(LANG(?propertyLabel ), "en"))

    	OPTIONAL {?value rdfs:label ?auxValue .}
    	BIND (IF(isLiteral(?value), ?value, ?auxValue) AS ?valueLabel)
    	FILTER (isNumeric(?valueLabel) ||
                    	LANGMATCHES(LANG(?valueLabel ), "en"))
    }
    """

	payload = {
    	'default-graph-uri': 'http://dbpedia.org', 
    	'query': query, 
    	'format': 'application/json', 
    	'timeout': 120000, 
    	'signal_void':'on', 
    	'signal_unconnected':'on' }

	response = requests.get(dbpedia_url, params=payload)

	return response.json()


# Write the information

def query2Text(entity, results = None):
	text = ""
	if results != None:
		for result in results["results"]["bindings"]:
			#text = text + entity +" has " + result["propertyLabel"]["value"].replace('\n', ' ').replace('\r', '') + ", that it is " + result["valueLabel"]["value"].replace('\n', ' ').replace('\r', '') + ". "
                    text = text + " The " + result["propertyLabel"]["value"].replace('\n', ' ').replace('\r', '') + " of " + entity + " is " + result["valueLabel"]["value"].replace('\n', ' ').replace('\r', '') + ". "
	return text
