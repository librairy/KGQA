import requests
from pprint import pprint

url = "http://query.wikidata.org/sparql"
query = "select ?ent where { ?ent wdt:P31 wd:Q11387 . ?ent wdt:P2120 ?obj } ORDER BY DESC(?obj)LIMIT 5"

payload = {
    'format': 'json', 
    'query': query
}

data = (requests.get(url, params = payload)).json()
#pprint(data)
#print(data['results']['bindings'][0]['ent']['value'])
#print(data['results']['bindings'][0]['ent']['value'].rsplit('/', 1)[-1])
for i in data['results']['bindings']:
    print(i['ent']['value'].rsplit('/', 1)[-1])