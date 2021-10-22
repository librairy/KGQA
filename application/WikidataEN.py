# Author: Rafael Ines Guillen
# Project: Explainable QA over KG
# File: DBèdia.py
# Purpose: solve questions to Wikidata in english


# Loading libraries and dependencies

import spacy

from SPARQLWrapper import SPARQLWrapper, JSON

from transformers import AutoTokenizer, TFAutoModelForQuestionAnswering
import tensorflow as tf


# Loading libraries and dependencies

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

print("Loading spacy model: tokenize, ner")
nlp = spacy.load("en_core_web_lg")
nlp.add_pipe('sentencizer')
# add pipeline (declared through entry_points in setup.py)
nlp.add_pipe("entityLinker", last=True)

print("Loaded")


print("Loding BERT model: bert-large-uncased-whole-word-masking-finetuned-squad")
tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
model = TFAutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
print("Loaded")
print("Ready to answer question from Wikidata in english:")


# Question treatment

def WikidataEN(question):
	print(question)

	doc = nlp(question)
	
	text = documentRetrieval(doc)

	return bertAnswer(question, text)


# Document retrieval

def documentRetrieval(doc):

	text = ""

	for ent in doc._.linkedEntities:
                print("entity-label:", ent.get_label())
                print("entity-id:",ent.get_id())
                results = relationFromEntity(ent.get_id())
                text = text + query2Text(ent.get_label(), results)
                # Second direction
                text = text + '\n'+ '\n'
                results = relationToEntity(ent.get_id())
                text = text + query2Text(ent.get_label(),results)

                print("summary: '",text)
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

    sparql.setQuery("""SELECT ?propertyLabel
                (GROUP_CONCAT(DISTINCT ?valueLabel;separator=", ") AS ?value)
            WHERE{
                ?item ?label"""+ ' \"'+entity+'\"@en .'+
                """?item ?prop ?value .
                ?property wikibase:directClaim ?prop .
                SERVICE wikibase:label {bd:serviceParam wikibase:language "en".
                                    ?property rdfs:label ?propertyLabel .
                                    ?value rdfs:label ?valueLabel .}
        }
        GROUP BY ?propertyLabel
    """)

    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


## Relation to the entity

def relationToEntity(entity):

    sparql.setQuery("""SELECT ?propertyLabel
                (GROUP_CONCAT(DISTINCT ?valueLabel;separator=", ") AS ?value)
            WHERE{
                ?item ?label"""+ ' \"'+entity+'\"@en .'+
                """?value ?prop ?item .
                ?property wikibase:directClaim ?prop .
                SERVICE wikibase:label {bd:serviceParam wikibase:language "en".
                                    ?property rdfs:label ?propertyLabel .
                                    ?value rdfs:label ?valueLabel .}
        }
        GROUP BY ?propertyLabel
    """)

    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


# Write the information

def query2Text(entity, results = None):
    text = ""
    if results != None:
        for result in results["results"]["bindings"]:
            text = text + entity +" has " + result["propertyLabel"]["value"].replace('\n', ' ').replace('\r', '') + ", that it is " + result["value"]["value"].replace('\n', ' ').replace('\r', '') + ". "
    return text

