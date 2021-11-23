import requests
from pprint import pprint

queryURL = "http://localhost:5000/eqakg/dbpedia/en?text=false"

questions = ["What tonality is Paganini's Caprice 24 written in?"]

for i in questions:
    
    files = {
        'question': (None, i),
    }

    response = requests.get(queryURL, files = files)

    pprint(response.json())