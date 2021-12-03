import requests
from pprint import pprint

queryURL = "http://localhost:5000/eqakg/dbpedia/en?text=true"

questions = ["count the number of people became famous for when Andrew Jackson was a commander ?"]

for i in questions:
    
    files = {
        'question': (None, i),
    }
    
    response = requests.get(queryURL, files = files)

    pprint(response.json())