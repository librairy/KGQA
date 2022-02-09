# Question Answering over Multiple and Heterogeneous Knowledge Bases


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Docker](https://img.shields.io/badge/docker-v20.10.2+-blue.svg)
![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![Task](https://img.shields.io/badge/task-EQAKG-green.svg)
[![License](https://img.shields.io/badge/license-Apache2-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

The MuHeQA (Multiple and Heterogeneous Question-Answering) system creates natural language answers from natural language questions using knowledge base from both structured (KG) and unstructured (documents) data sources.


```bibtex
@inproceedings{paper2022,
  title={MuHeQA: Question Answering over Multiple and Heterogeneous Knowledge Bases},
  author={xxx},
  booktitle={xxx},
  url={https://xxx},
  year={2022}
}
```

## Preparation

1. Prepare a [Python 3](https://www.python.org/downloads/release/python-395/) environment with  [Conda](https://docs.conda.io) installed
1. Clone this repo
	  ```
	  git clone https://github.com/librairy/MuHeQA.git
	  ```
1. Move into the root directory.
    ```
	  cd MuHeQA
	  ```
1. Download the [RDF Verbalizer model](https://delicias.dia.fi.upm.es/nextcloud/index.php/s/bRxnH93Df9Psaeo) into the `application/summary/kg/nlg/model` folder
    ```
    wget -O application/summary/kg/nlg/model/pytorch_model.bin https://delicias.dia.fi.upm.es/nextcloud/index.php/s/bRxnH93Df9Psaeo/download
    ```
1. Download the [answer classifier](https://delicias.dia.fi.upm.es/nextcloud/index.php/s/Jp5FeoBn57c8k4M) and unzip into the root project directory. The folder `resources_dir/` is created.
    ```
    wget -O resources.zip https://delicias.dia.fi.upm.es/nextcloud/index.php/s/Jp5FeoBn57c8k4M/download
    unzip resources.zip
    ```
1. Install dependencies (in case you have a device based on Apple's M1 chip skip to the [M1 Environment](#m1-environment) step):    
		```
		pip install -r requirements.txt
		```
### M1 Environments (only for Apple's M1 devices )
1. Install the Apple edition of `tensorflow`
    ````
    pip install --upgrade --force --no-dependencies tensorflow-macos
    pip install --upgrade --force --no-dependencies tensorflow-metal
    `````
1. Compile and install the `tokenizers` module from Huggingface:
    ````
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    cd /Users/cbadenes/Projects
    git clone https://github.com/huggingface/tokenizers
    cd tokenizers/bindings/python
    pip install setuptools_rust
    python setup.py install
    `````
1. Compile and install the `transformers` module from Huggingface:
    ````
    pip install git+https://github.com/huggingface/transformers
    `````
1. And finally, install the rest of dependencies:
    ````
    pip install -r min-requirements.txt    
    ````

## Service start-up

1. Once the environment is ready, just execute the following command (`runserver` for development mode and `runprodserver` for production mode ):
    ```
    python manage.py runserver
    ```
1.  It may take some minutes to load some external resources. The following logs will appear when everything is ready:

    ```
    Loading RDF2nlg model: /Users/cbadenes/Projects/muheqa/application/summary/kg/nlg/model ..
    model ready
    Linked to DBpedia(en): http://dbpedia.org/sparql
    Linked to Wikidata (en): http://query.wikidata.org/sparql
    Ready to answer question from the English edition of CORD-19 collection
    Loading bert-large-uncased-whole-word-masking-finetuned-squad model..
    model ready
    Loading deepset/roberta-base-squad2-covid model..
    model ready
    Loading deepset/roberta-base-squad2 model..
    model ready
    English answerer is ready
     * Serving Flask app "application.app" (lazy loading)
     * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
     * Debug mode: off
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ```


## Server routes

The message body must contain the `question` field with the natural language question, and the query parameter `evidence` sets whether the summary generated has to be retrieved or not.

The availabe URIs are:
- `/muheqa/dbpedia` : solve questions using the English edition of DBpedia.
- `/muheqa/wikidata`: solve questions using the English edition of Wikidata.
- `/muheqa/cord19`: solve questions using the Covid-19 Open Research Dataset.
- `/muheqa/all`: solve questions using all sources of information.


## Example

To answer the question *Where was Fernando Alonso born?* using DBpedia:

   ```
    curl --location --request GET 'http://127.0.0.1:5000/muheqa/dbpedia/en?evidence=false' --form 'question="Where was Fernando Alonso born?"'
   ```

And the response:

   ```
   {
	"answer": "Oviedo, Asturias, Spain",
	"confidence": 0.801,
	"evidence": {
		"end": 149,
		"summary": "  The car number of Fernando Alonso is 14.   The Last win of Fernando Alonso is 2013.   The birth place of Fernando Alonso is Oviedo, Asturias, Spain.   The name of Fernando Alonso is Fernando Alonso.   The First win of Fernando Alonso is 2003.   The last season of Fernando Alonso is 2018.   The birth name of Fernando Alonso is Fernando Alonso D\u00edaz.   The caption of Fernando Alonso is Alonso in 2016.   The First race of Fernando Alonso is 2001.   The image size of Fernando Alonso is 240.   The last win of Fernando Alonso is 2013 Spanish Grand Prix.   The nationality of Fernando Alonso is Spanish.   The title of Fernando Alonso is Fernando Alonso achievements, Fernando Alonso teams and series.   The first race of Fernando Alonso is 2001 Australian Grand Prix.   The 2021 Team of Fernando Alonso is Alpine F1, Renault in Formula One.   The source  of Fernando Alonso is Alonso's race engineer at Ferrari, Andrea Stella, on Alonso's ability and similarities to Michael Schumacher.   The first win of Fernando Alonso is 2003 Hungarian Grand Prix.  .  ",
		"start": 126
	},
	"question": "where was Fernando Alonso born?"
}
   ```
