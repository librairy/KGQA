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

1. Prepare an environment with [Python 3](https://www.python.org/downloads/release/python-395/) and [Conda](https://docs.conda.io)
1. Clone this repo
	  ```
	  git clone https://github.com/librairy/MuHeQA.git
	  ```
1. Move into the root directory.
    ```
	  cd MuHeQA
	  ```
1. Download the [RDF Verbalizer model](https://delicias.dia.fi.upm.es/nextcloud/index.php/s/bRxnH93Df9Psaeo) into the `application/summary/kg/nlg/model` folder
1. Download the [answer classifier](https://delicias.dia.fi.upm.es/nextcloud/index.php/s/Jp5FeoBn57c8k4M) and unzip into the root project directory. The folder `resources_dir/` is created.
1. Create a new `conda` environment from the `environment.yml` file:
    ```
    conda env create -f environment.yml
    ```
1. Activate the environment:
		```
		conda activate .muheqa
		```
1. In case you have a device based on Apple's M1 chip skip to [M1 Environment](#m1-environment) step
1. Install the dependencies:
		```
		pip install -r requirements.txt
		```
### M1 Environments (only for Apple's M1 devices )
1. Install the Apple edition of `tensorflow`
    ````
    pip install --upgrade --force --no-dependencies tensorflow-macos
    pip install --upgrade --force --no-dependencies tensorflow-metal
    `````
1. Install the following libraries:
    ````
    pip install Flask==1.1.4
    pip install Flask-Cors==3.0.10
    pip install Flask-Script==2.0.6

    pip install spacy
    pip install spacy-dbpedia-spotlight==0.2.1
    pip install spacy-entity-linker==1.0.1
    pip install spacy-legacy==3.0.8
    ````
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
1. And finally, install `torch` and `keras`
    ````
    pip install flatbuffers
    pip install keras==2.6.0
		pip install torch
    ````

## Service start-up

1. Once the environment is ready, just execute the following command (`runserver` for development mode and `runprodserver` for production mode ):
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

The message body must contain the `question` field with the natural language question, and the query parameter `evidence` sets whether the summary generated has to be retrieved or not.

The availabe URIs are:
- `/muheqa/dbpedia/en` : solve questions using the English edition of DBpedia.
- `/muheqa/dbpedia/es` : solve questions using the Spanish edition of DBpedia.
- `/muheqa/wikidata/en`: solve questions using the English edition of Wikidata.
- `/muheqa/wikidata/es`: solve questions using the Spanish edition of Wikidata.
- `/muheqa/wikidata/en`: solve questions using the English edition of Wikidata.


## Example

To answer the question *Where was Fernando Alonso born?* using DBpedia:

   ```
    curl --location --request GET 'http://127.0.0.1:5000/muheqa/dbpedia/en?evidence=false' --form 'question="Where was Fernando Alonso born?"'
   ```

And the response:

   ```
   {
     "answer":"oviedo, asturias, spain",
     "question":"Where was Fernando Alonso born?",
     "textLen":10143
   }
   ```
