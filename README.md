# explainable-qa
Knowledge Graph Question-Answering


## Abstract
Creation of an Extractive Question/Answering (EQA) system that continuously updates its knowledge from a KG. The student will use language models (e.g. BERT) to build a RESTful service that responds to natural language queries.

## Files

The api files in order are:
 - application:
 	- [app.py](application/app.py) : controls the requests and responses of the API.
 	- [config.py](application/config.py) : contains the differents configurations for the API.
 	- [DBpedia.py](application/DBpedia.py) : solve questions to DBpedia in english.
 	- [DBpediaES.py](application/DBpediaES.py) : solve questions to DBpedia in spanish.
 	- [Wikidata.py](application/Wikidata.py) : solve questions to Wikidata in english.
 - [manage.py](manage.py) : main python file with several command options for managing the database and starting the server.
 - [requirements.txt](requirements.txt) : the libraries needed for the proper operation of the server.


## Set up

The latest Python version checked is [3.9.5](https://www.python.org/downloads/release/python-395/) and it is required to be 64 bit (compatible with TensorFlow library). 

To install the libraries and dependencies:
`pip install -r requirement.txt`


## Start the API

The [manage.py](manage.py) file, which it is the main python file of the api, allows to config and start the API with the command line. Possibles functions are:
 - **Development mode**: starts the development server. Optionals parameters: host (-h, --host), port (-p, --port).
<br/>`python manage.py runserver`
 - **Production mode**: starts the production server. Optionals parameters: host (-h, --host), port (-p, --port).
<br/>`python manage.py runprodserver`
 - **Help**: prints the commands with their description.
<br/>`python manage.py -?`
<br/>It could be used with others commands to get more info of them. For example:
<br/>`python manage.py runserver -?`


## Server routes

The [app.py](application/app.py) file controls the flask server in production and development mode. The differents URIs and methods allowed in the server are:
- /DBpedia : solve questions to DBpedia in english.
	- Method: GET
	- Request: question in the body and the parameter text (with true value) if you want to request the full text.
	- Response: json object with the answer, question and text if requested.
	- Status code: 200
- /DBpediaES : solve questions to DBpedia in spanish.
	- Method: GET
	- Request: question in the body and the parameter text (with true value) if you want to request the full text.
	- Response: json object with the answer, question and text if requested.
	- Status code: 200
- /Wikidata : solve questions to Wikidata in english.
	- Method: GET
	- Request: question in the body and the parameter text (with true value) if you want to request the full text.
	- Response: json object with the answer, question and text if requested.
	- Status code: 200


## Example

To answer the question *Where was Fernando Alonso born?* with DBpedia as KG:

`curl --location --request GET 'localhost:5000/dbpedia/en?text=true' \
--form 'question="Where was Fernando Alonso born?"'`

And the response (without text for saving space):

`{
    "answer": "oviedo, asturias, spain",
    "question": "Where was Fernando Alonso born?"
}`


## Documentation
Documentation in spanish Latex : https://www.overleaf.com/read/zmtfzwzqtvtz

