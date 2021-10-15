import requests
from pprint import pprint

queryURL = "http://localhost:5000/dbpedia/en"

questions = ["Who is the pole driver of 1992 Canadian Grand Prix?"]

for i in questions:
    
    files = {
        'question': (None, i),
    }

    response = requests.get(queryURL, files = files)

    pprint(response.json())