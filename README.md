# ExtractiveQA over Knowledge Graphs


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Docker](https://img.shields.io/badge/docker-v20.10.2+-blue.svg)
![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![Task](https://img.shields.io/badge/task-EQAKG-green.svg)
[![License](https://img.shields.io/badge/license-Apache2-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

## Basic Overview

Web service that creates natural language answers from natural language questions using as knowledge base a combination of structured (KG) and unstructured (documents) data. 

## Quick Start (based on a Docker environment)

Let's explore DBpedia through natural language questions:

1. Install [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/install/)
1. Clone this repo

	```
	git clone https://github.com/librairy/EQAKG.git
	```
1. Move into `EQAKG` directory.
    ```
	cd EQAKG
	```
1. Start the web service by running docker:
    ````
    docker-compose up -d
    docker-compose logs -f
    ````
1.  It may take some minutes to load some external resources. The following logs will appear when everything is ready:

    ````
    kgqa             | 16:31:28: Indexer    : loading word embeddings
    qg               | 2021-03-02 16:50:21,488 - kb.dbpedia - INFO - bloom file: ./data/blooms/spo2True.bloom does not exist. Creating an empty bloom file
    qg               | 2021-03-02 16:50:21,489 - kb.dbpedia - INFO - bloom file: ./data/blooms/spo2False.bloom does not exist. Creating an empty bloom file
    qg               | 2021-03-02 16:50:21,489 - kb.dbpedia - INFO - Number of bloom entries: 2
    qg               | KB <kb.dbpedia.DBpedia object at 0x7efb94c6ad00>
    qg               | 2021-03-02 16:50:21,571 - __main__ - INFO - Starting the HTTP server at localhost:5000/qg/api/v1.0/query
    kgqa             | 16:33:40: Indexer    : embedding model available
    kgqa             | 16:33:40: loading index..
    kgqa             | 16:33:40: loading resources..
    kgqa             | 16:33:40: resources loaded
    kgqa             | 16:33:45: Main    : Endpoint:[ sparql-endpoint:https://dbpedia.org/sparql, kg:http://dbpedia.org, qg_service:query-generator:5000/qg/api/v1.0/query, qg_graph:dbpedia]
    kgqa             | 9186 resources successfully indexed in 00:02:12
    kgqa             | Linker ready
    kgqa             |  * Serving Flask app "app" (lazy loading)
    kgqa             |  * Environment: production
    kgqa             |  * Debug mode: off
    kgqa             | 16:33:45:  * Running on http://0.0.0.0:5001/ (Press CTRL+C to quit)
    ````


## Local Set up (based on a Python environment)

If you prefer to start the service via a Python environment instead of using Docker images, you will need to have Python version [3.9.5](https://www.python.org/downloads/release/python-395/) 64-bit installed: 

1. Clone this repo

	```
	git clone https://github.com/librairy/EQAKG.git
	```
1. Move into `EQAKG` directory.
    ```
	cd EQAKG
	```
1. Create a virtual environment:
    ```
    python3 -m venv eqakg-env
    ```
1. Activate the virtual environment:
    ```
    source eqakg-env/bin/activate
    ```    
1. Install the dependencies:
    ```
    pip install -r requirement.txt
    ```
1. Download and unzip the following [file](https://delicias.dia.fi.upm.es/nextcloud/index.php/s/Jp5FeoBn57c8k4M) in the project directory. It contains the models used by the service. The folder 'resources_dir' is created.
1. Run the service (`runserver` for development mode and `runprodserver` for production mode ):
    ```
    python manage.py runserver
    ```
1.  It may take some minutes to load some external resources. The following logs will appear when everything is ready:

    ```
    Answering for predictions without further training.
    Loaded
    Ready to answer question from Wikidata in english:
     * Serving Flask app "application.app" (lazy loading)
     * Environment: production
        WARNING: This is a development server. Do not use it in a production deployment.
        Use a production WSGI server instead.
     * Debug mode: off
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ```

## Server routes

The message body must contain the `question` field with the natural language question, and the query parameter `text` sets whether the summary generated has to be retrieved or not.

The availabe URIs are:
- `/eqakg/dbpedia/en` : solve questions using the English edition of DBpedia.
- `/eqakg/dbpedia/es` : solve questions using the Spanish edition of DBpedia.
- `/eqakg/wikidata/en`: solve questions using the English edition of Wikidata.


## Example

To answer the question *Where was Fernando Alonso born?* using DBpedia:

   ```
    curl --location --request GET 'localhost:5000/eqakg/dbpedia/en?text=false' --form 'question="Where was Fernando Alonso born?"'
   ```

And the response:

   ```
   {
     "answer":"oviedo, asturias, spain",
     "question":"Where was Fernando Alonso born?",
     "textLen":10143
   }
   ```


