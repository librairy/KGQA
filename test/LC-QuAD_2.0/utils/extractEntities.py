import json
import requests
from pprint import pprint
import multiprocessing as mp
from urllib.request import urlopen
import traceback
from copy import deepcopy
import pandas as pd
import csv
import re

def jsonToDict(route) -> dict:
    '''
    Funcion auxiliar que dada la ruta de un json, lo abre y lo convierte a lista de diccionarios
    '''
    with open(route, encoding="utf-8") as f:
        return json.load(f)

def queryJson(queryURL, query):
    '''
    Funcion auxiliar que dado un JSON con una pregunta, realiza una consulta (con esta pregunta) a una URL dada
    '''
    payload = {
        'format': 'json', 
        'query': query
    }

    #Header con User-Agent (protocolo de seguridad de WikiData)"
    headers = {
        'User-Agent': "LibrAIry/EQAKG (https://librairy.github.io/; josevegra@hotmail.com) <librAIry/EQAKG>/0.1",
    }

    try:
        jsonResponse = requests.get(queryURL, params = payload, headers = headers)
        return jsonResponse.json()
    except:
        print("query: ", query)
        print("Unable to convert response to json or incorrect query sintax")
        pprint(jsonResponse)
        return


def writeIntoJson(rows, resultsRoute, append):
    '''
    Funcion auxiliar que agrega datos a un archivo json (lista de json objects)
    '''
    if not append:
        with open(resultsRoute,'w', newline='', encoding="utf-8") as f:
            csvwriter = csv.writer(f,delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            global header
            csvwriter.writerow(header)
            f.close()    

    with open(resultsRoute, 'a', newline='', encoding="utf-8") as f:
        df = pd.DataFrame(deepcopy(rows))
        df.to_csv(f, header=False, index=False, sep=';', quoting=csv.QUOTE_ALL)
        rows[:] = []
        f.close()


def createDictionary(question, query, QID, entities):
    '''
    Funcion auxiliar que crea el diccionario que posteriormente usaremos como dataframe
    '''
    return { "question" : question, "query" : query, "QID" : QID, "entities" : entities }

def checkAndWrite(dict, counter, rows, resultsRoute):
    rows.append(dict)
    counter.value += 1
    #print("Counter: ", counter.value)
    #Escribimos cuando el valor del contador llegue a 24
    if(counter.value == 24):
        writeIntoJson(rows,resultsRoute,append=False)
    elif(counter.value != 0 and counter.value % 24 == 0):
        #print("Escribiendo. Contador: ", counter.value)
        writeIntoJson(rows,resultsRoute,append=True)

def QIDtoEntity(query,QIDList,entityList):
    for i in QIDList:
        jsonURL = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + i + "&format=json"
        response = urlopen(jsonURL)
        jsonEntityData = json.loads(response.read())
        
        if "en" in jsonEntityData["entities"][i]["labels"].keys():
            entityList.append(jsonEntityData["entities"][i]["labels"]["en"]["value"])
        else:
            try:
                lang = list(jsonEntityData["entities"][i]["labels"].keys())[0]
                entityList.append(jsonEntityData["entities"][i]["labels"][lang]["value"])
            except:
                print("query: ", query)
                pprint(lang)
                traceback.print_exc()
            


def fillDictionary(i, query, rows, counter, jsonResponse, resultsRoute):

    #Si la consulta SPARQL es de tipo ask, la respuesta es un booleano
    if "ask" in query.lower():
        dict = createDictionary(i["NNQT_question"], query, " ", jsonResponse["boolean"])
        #pprint(dict)
        checkAndWrite(dict, counter, rows, resultsRoute)       
        return
        
    queriedValue = (query.split("?")[1].split(" ")[0])

    QIDList = []
    answerList = []
    
    for j in jsonResponse['results']['bindings']:
        if queriedValue == "sbj":
            if "sbj_label" in query.lower():
                answerList.append(j["sbj_label"]['value'])
            else:
                QIDList.append(j[queriedValue]['value'].rsplit('/', 1)[-1])
        else:
            if "?value " in query.lower():
                answerList.append(j["value"]['value'])
            elif(re.search("Q[1-9]", j[queriedValue]['value'])) != None:
                QIDList.append(j[queriedValue]['value'].rsplit('/', 1)[-1])
            else:
                answerList.append(j[queriedValue]['value'])

    if(len(answerList) == 0) and (len(QIDList) > 0):
        QIDtoEntity(query,QIDList,answerList)

    dict = createDictionary(i["NNQT_question"], query, QIDList, answerList)
    #pprint(dict)
    checkAndWrite(dict, counter, rows, resultsRoute)


def parseQuery(resultsRoute,i,rows,counter,queryURL):

    query = i["sparql_wikidata"]

    jsonResponse = queryJson(queryURL, query)

    fillDictionary(i, query, rows, counter, jsonResponse, resultsRoute)


def extractEntities(pool,rows,counter,jsonRoute,queryUrl,resultsRoute):   
    LCJson = jsonToDict("test.json")

    for i in LCJson:       
        pool.apply_async(parseQuery, (resultsRoute,i,rows,counter,queryURL))
    
    pool.close()
    pool.join()

    #Escribimos lo que quede
    writeIntoJson(rows, resultsRoute)

header = ["Question", "Query", "QIDs", "Entities/Answer"]

if __name__ == '__main__':

    with mp.Manager() as manager:

        rows = manager.list([])
        counter = manager.Value('i', 0)

        pool = mp.Pool(processes=6, initargs = (counter,rows,))

        queryURL = "http://query.wikidata.org/sparql"

        extractEntities(pool,rows,counter,"test.json",queryURL,"results/Entities.csv")