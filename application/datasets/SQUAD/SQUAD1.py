import spacy_dbpedia_spotlight

import spacy
from spacy.lang.en.examples import sentences 

from SPARQLWrapper import SPARQLWrapper, JSON

from transformers import AutoTokenizer, TFAutoModelForQuestionAnswering
import tensorflow as tf

import json
import csv


# Loading libraries and dependencies
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

print("Loading SpaCy model")
nlp = spacy.blank('en')
nlp.add_pipe('dbpedia_spotlight')
print("Loaded")

print("Loding BERT model: bert-large-uncased-whole-word-masking-finetuned-squad")
tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
model = TFAutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
print("Loaded")




# Extractive QA

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

	return answer


# Informationretrival

def informationRetrieval(doc):

	text = ""

	for ent in doc.ents:
		results = relationFromEntity(ent.kb_id_)
		text = text + query2Text(ent.text, results)
		return text


# Query part

## Relation from the entity

def relationFromEntity(entity):
	sparql.setQuery("PREFIX dbr: <http://dbpedia.org/resource/> \n" + 
	"SELECT ?propertyLabel (GROUP_CONCAT(DISTINCT ?valueLabel ; SEPARATOR=\", \") AS ?valueLabel ) {\n"+
		
		"<" + entity + """> ?property ?value .
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
	""")

	sparql.setReturnFormat(JSON)
	return sparql.query().convert()


# Write the information

def query2Text(entity, results = None):
	text = ""
	if results != None:
		for result in results["results"]["bindings"]:
			text = text + entity +" has " + result["propertyLabel"]["value"].replace('\n', ' ').replace('\r', '') + ", that it is " + result["valueLabel"]["value"].replace('\n', ' ').replace('\r', '') + ". "
	return text



# Main

# Test-SQUAD1.csv will be created in the same folder as the SQUAD1.py
with open('Test-SQUAD1.csv', mode='w', encoding='utf-8', newline='') as question_file:
	fieldnames = ['question', 'answer', 'text']
	writer = csv.DictWriter(question_file, fieldnames=fieldnames)

	writer.writeheader()
	# text.json is the name of the test set of the SQUAD dataset
	f = open('test.json',)
	data = json.load(f)

	missedQuestion = 0

	for i in data:
		if(str(i['corrected_question']) != "[]"):
			question = i['corrected_question']
			error = False
			try:
				doc = nlp(question)
			except ValueError:
				error = True
				missedQuestion += 1
				writer.writerow({'question': question, 'answer': '[Error spacy]', 'text': ''})
			if not error:
				text = informationRetrieval(doc)
				answer = bertAnswer(question, text)
				writer.writerow({'question': question, 'answer': answer, 'text': text})
		else:
			missedQuestion += 1

	print('The number of missed question are: ' + str(missedQuestion))

