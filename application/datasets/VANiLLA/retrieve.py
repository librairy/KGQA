import requests
import json
import csv
import re
import time
import multiprocessing as mp
import pandas as pd

def JSONLineToDict(JSONRoute):
    '''
    Funcion auxiliar que dado un archivo json con JSONObjects en cada linea,
    lo abre y lo convierte a lista de diccionarios
    '''  
    with open(JSONRoute) as f:
        jsonList = list(f)
    
    return json.loads(json.dumps([json.loads(jsonLine) for jsonLine in jsonList]))

def queryJSON(queryURL, questionDict):
    '''
    Funcion auxiliar que dado un JSON con una pregunta, realiza una consulta (con esta pregunta) a una URL
    '''
    question = questionDict['question']
    files = {
        'question': (None, question),
    }
    response = requests.get(queryURL, files = files)
    #pprint(response.json())
    #Obtenemos la respuesta como JSonObject y la devolvemos
    return response.json()

def writeResults(csvRoute, rows, counter, question, modelAnswer, obtainedAnswer, queryTime, text):  
    '''
    Funcion auxiliar que extrae la respuesta que se espera
    '''    
    #La respuesta esperada se obtiene con una expresion regular (sacar texto entre corchetes)
    if obtainedAnswer is None:
        obtainedAnswer = "None"
    
    rows.append( [question, modelAnswer, obtainedAnswer, queryTime, text] )
    counter.value += 1
    #print("Contador: ", counter.value)

    #Escribimos cuando el valor del contador llegue a 24
    if(counter.value % 24 == 0):
        #print("Escribiendo. Contador: ", counter.value)
        with open(csvRoute, 'a', newline='', encoding="utf-8") as f:
            (pd.DataFrame.from_records(rows, columns=header)).to_csv(f, header=False, index=False, sep=';', quoting=csv.QUOTE_ALL)
            rows[:] = []
            f.close()

def answerQuestion(csvRoute, questionDict, rows, counter, queryURL):
    '''
    Funcion auxiliar para paralelizar la ejecucion de consultas y escritura en csv de resultados. Realiza la consulta (midiendo el tiempo que tarda) y llama a writeResults
    '''
    #print("Process id: ", os.getpid())
    #print("Question: ", i['question']) 
    #Para medir el tiempo que se tarda en ejecutar la consulta
    queryStartTime = time.time()

    #Obtenemos la respuesta json del sistema de QA.
    jsonResponse = queryJSON(queryURL,questionDict)

    queryTime = round((time.time() - queryStartTime),2)

    text = jsonResponse['evidence']
    evidence = jsonResponse['result']
    if evidence != "":
        text = re.sub(evidence, "[" + evidence + "]", text)
    
    #Pasamos las respuestas a minuscula y llamamos a writeResults.
    writeResults(csvRoute, rows, counter, questionDict['question'], questionDict['answer'].lower(),jsonResponse['answer'].lower(),queryTime,text.lower())

def retriever(pool, rows, counter, JSONroute, queryURL, csvRoute, writeHeader = False):
    '''
    Funcion que dado un JSON con preguntas y respuestas, una url a través de la cual realizar consultas y un csv donde guardar los resultados, 
    obtiene la respuesta a la pregunta y la vuelca junto al texto a partir del cual se genero en un CSV
    '''
    dataset = JSONLineToDict(JSONroute)

    #Escribimos el Header
    if writeHeader:
        with open(csvRoute,'w', newline='', encoding="utf-8") as f:

            csvwriter = csv.writer(f,delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            global header
            csvwriter.writerow(header)
            f.close()
        
    for i in dataset:
        #Paraleliza con metodos asincronos
        pool.apply_async(answerQuestion, (csvRoute,i,rows,counter,queryURL))

    pool.close()
    pool.join()

    #Escribimos lo que quede
    with open(csvRoute, 'a', newline='', encoding="utf-8") as f:
        (pd.DataFrame.from_records(rows, columns=header)).to_csv(f,header=False, index=False, sep=';', quoting=csv.QUOTE_ALL)
        f.close()

#Creamos el array donde guardaremos las columnas y el contador como variables globales para que sean accesibles por los multiprocesos
rows = None
counter = None
header = ["Question", "Answer", "Response", "Time","Evidence"]

if __name__ == '__main__':

    with mp.Manager() as manager:

        rows = manager.list([])
        counter = manager.Value('i', 0)

        pool = mp.Pool(processes=6, initargs = (counter,rows,))

        queryUrl = "http://localhost:5000/eqakg/dbpedia/en?evidence=true"
        #queryUrl = "https://librairy.linkeddata.es/eqakg/dbpedia/en?text=false" 

        retriever(pool,rows,counter,"data/Vanilla_Dataset_Test.json",queryUrl,"results/VANiLLA.csv", writeHeader=True)