import requests
from pprint import pprint

queryURL = "https://librairy.linkeddata.es/eqakg/dbpedia/en?text=false"

questions = ["Where was Fernando Alonso born?"]

for i in questions:
    
    files = {
        'question': (None, i),
    }

    response = requests.get(queryURL, files = files)

    pprint(response.json())