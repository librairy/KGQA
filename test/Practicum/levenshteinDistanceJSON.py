import requests
import json
import enchant
import csv
import re
import time

def jsonToDict(route) -> dict:
    '''
    Funcion auxiliar que dada la ruta de un json, lo abre y lo convierte a diccionario
    '''
    with open(route, encoding="utf-8") as f:
        return json.load(f)

def queryJSON(queryURL, json):
    '''
    Funcion auxiliar que dado un JSON con una pregunta, realiza una consulta (con esta pregunta) a una URL
    '''
    question = json['question']
    files = {
        'question': (None, question),
    }
    '''
    En caso de que quisiesemos la respuesta verbalizada o larga, hacer la request con params = payload:
    payload = {
        ('text', 'true')
    }
    '''
    response = requests.get(queryURL, files = files)
    #Obtenemos la respuesta como JSonObject y la devolvemos
    return response.json()

def writeResults(csvwriter, question, modelAnswerLong, obtainedAnswer, queryTime, textLen):  
    '''
    Funcion auxiliar que extrae la respuesta que se espera, hace la distancia de levenshtein y escribe en el csv:
    -Pregunta
    -Respuesta modelo y nuestra respuesta
    -Distancia de levenshtein entre ambas respuestas
    -Tiempo que ha tardado en ejecutarse la consulta
    -Longitud del texto del que se ha obtenido nuestra respuesta
    -Si la pregunta dada tiene respuesta modelo o no
    '''    
    #La respuesta esperada se obtiene con una expresion regular (sacar texto entre corchetes)
    modelAnswerLongGroups = re.search(r"\[([^\)]+)\]", modelAnswerLong)
    if(modelAnswerLongGroups is not None):

        modelAnswer = modelAnswerLongGroups.group(1)
        isAnswered = "YES"
        if modelAnswer == "answer":
            isAnswered = "NO" 
        distance = "None"
        if obtainedAnswer is not None:
            distance = enchant.utils.levenshtein(modelAnswer,obtainedAnswer)
        csvwriter.writerow( [question, modelAnswer, obtainedAnswer, distance , queryTime, textLen, isAnswered] )

def compareAnswersJSON(JSONroute, queryURL, csvRoute):
    '''
    Función que dado un JSON con preguntas y respuestas (asumimos que las preguntas están en la clave 'question' del JSON, y las respuestas en 'verbalized_answers'), 
    una url a través de la cual realizar consultas y un csv donde guardar los resultados:
    - Realiza las preguntas del JSON dado
    - Lo compara con la respuesta esperada segun la Distancia de Levenshtein
    - Guarda en el CSV la pregunta, la respuesta esperada, la respuesta obtenida y varias metricas de rendimiento
    '''
    VQuandaData = jsonToDict(JSONroute)

    with open(csvRoute,'w', newline='', encoding="utf-8") as f:

        csvwriter = csv.writer(f,delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)

        #Escribimos el Header
        csvwriter.writerow( ["Question", "Answer", "Response", "Levenshtein Distance","Query Time","Text Length","Is Answered"])

        for i in VQuandaData:

            #Para medir el tiempo que se tarda en ejecutar la consulta
            queryStartTime = time.time()
            jsonResponse = queryJSON(queryURL,i)
            queryTime = round((time.time() - queryStartTime),2)

            #Pasamos las respuestas a minuscula y llamamos a extractAndCompare.
            writeResults(csvwriter, i['question'], i['verbalized_answer'].lower(),jsonResponse['answer'].lower(),queryTime,jsonResponse['textLen'])

        f.close()
        
compareAnswersJSON("train.JSON","http://localhost:5000/dbpedia/en","levenshtein.csv")