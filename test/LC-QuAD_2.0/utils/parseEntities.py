import pandas as pd
import re
from urllib.request import urlopen
import json
from pprint import pprint
import traceback
import csv

def extractEntities(testString):
    testString = re.sub('[\[\]\'\']', '', testString)

    testMatch = re.search("http://www.wikidata.org/entity/Q", testString)
    res = ""

    if testMatch != None :
        testArray = testString.split(", ")
        for counter,i in enumerate(testArray):
            qid = i.split("http://www.wikidata.org/entity/")[1]
            jsonURL = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + qid + "&format=json"
            response = urlopen(jsonURL)
            jsonEntityData = json.loads(response.read())
            
            if "en" in jsonEntityData["entities"][qid]["labels"].keys():
                entity = jsonEntityData["entities"][qid]["labels"]["en"]["value"]
            else: 
                try:
                    lang = list(jsonEntityData["entities"][qid]["labels"].keys())[0]
                    entity = jsonEntityData["entities"][qid]["labels"][lang]["value"]
                except:
                    print("algo")
                    pprint(lang)
                    traceback.print_exc()

            if counter == 0:
                res = entity
            else:
                res = res + ", " + entity
        
        return res 

    else:
        return testString

df = pd.read_csv("results/Entities.csv", sep=";")

df['Question'] = df['Question'].map(lambda line : re.sub('[<>{}]', '', line))

df['QIDs'] = df['QIDs'].map(lambda line : re.sub('[\[\]\'\']', '', line))

df['Entities/Answer'] = df['Entities/Answer'].map(extractEntities) 

df.to_csv("results/LC-Quad_Dataset.csv", sep=";", index = False, quoting=csv.QUOTE_ALL)