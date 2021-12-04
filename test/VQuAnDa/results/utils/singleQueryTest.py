import requests
from pprint import pprint

queryURL = "http://localhost:5000/eqakg/wikidata/en?text=false"

questions = ["what city was alex golfis born in"]

for i in questions:
    
    files = {
        'question': (None, i),
    }
    
    response = requests.get(queryURL, files = files)

    pprint(response)