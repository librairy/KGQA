import json
import requests
from pprint import pprint
from urllib.request import urlopen
import re

def jsonToDict(route) -> dict:
    '''
    Funcion auxiliar que dada la ruta de un json, lo abre y lo convierte a lista de diccionarios
    '''
    with open(route, encoding="utf-8") as f:
        return json.load(f)

def QIDtoEntity(QIDList,entityList):
    for i in QIDList:
        jsonURL = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + i + "&format=json"
        response = urlopen(jsonURL)
        jsonEntityData = json.loads(response.read())
        entityList.append(jsonEntityData["entities"][i]["labels"]["en"]["value"])
        
def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield (key, value)
            yield from recursive_items(value)
        else:
            yield (key, value)


url = "http://query.wikidata.org/sparql"
query = [
"SELECT ?answer WHERE { wd:Q242542 wdt:P20 ?answer . ?answer wdt:P1376 wd:Q110888}"
]

for i in query:

    payload = {
        'format': 'json', 
        'query': i
    }
    
    jsonResponse = (requests.get(url, params = payload))
    #pprint(jsonResponse.content)
    jsonResponse = jsonResponse.json()
    pprint(jsonResponse)
    queriedValue = (i.split("?")[1].split(" ")[0])

    for j in jsonResponse['results']['bindings']:
        if queriedValue == "sbj":
            if "sbj_label" in query[0].lower():
                print(j["sbj_label"]['value'])
            else:
                print(j[queriedValue]['value'].rsplit('/', 1)[-1])
        elif queriedValue == "ent":
            print(j[queriedValue]['value'].rsplit('/', 1)[-1])
        else:
            print(j[queriedValue]['value'])


a = {
    'a': {"b": {"c": 2, 
              "d": 4}, 
          "e": {"f": 6}
        }

}


for key, value in recursive_items(a):
    if (key == "b"):
        print(key, value)


for k, v in a.items():
    for k1, v1 in v.items():
        print(k1)

#QIDtoEntity(["Q42493"],[""])