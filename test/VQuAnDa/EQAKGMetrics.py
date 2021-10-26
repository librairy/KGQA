import requests
import json
import enchant
import csv
import re
import time
import itertools
from sacrebleu import sentence_bleu
import multiprocessing as mp

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

def exactMatchScore(string1,string2):
    '''
    Funcion auxiliar que incorpora la medida EM (exact match)
    '''
    matches = 0
    total = 0
    for (x,y) in itertools.zip_longest(string1,string2):
        if(x == y):
            matches+=1
        total+=1
    return matches/total

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
            reference = modelAnswer.split()
            candidate = obtainedAnswer.split()

        csvwriter.writerow( [question, modelAnswer, obtainedAnswer, distance, sentence_bleu(obtainedAnswer,[modelAnswer]).score, exactMatchScore(reference,candidate), queryTime, textLen, isAnswered] )

def evaluateQuestion(i,queryURL,csvwriter):
    '''
    Funcion auxiliar para paralelizar la ejecucion de consultas y escritura en csv de resultados. Realiza la consulta (midiendo el tiempo que tarda) y llama a writeResults
    '''
    #Para medir el tiempo que se tarda en ejecutar la consulta
    queryStartTime = time.time()
    jsonResponse = queryJSON(queryURL,i)
    queryTime = round((time.time() - queryStartTime),2)

    #Pasamos las respuestas a minuscula y llamamos a extractAndCompare.
    writeResults(csvwriter, i['question'], i['verbalized_answer'].lower(),jsonResponse['answer'].lower(),queryTime,jsonResponse['textLen'])

def EQAKGMetrics(pool, JSONroute, queryURL, csvRoute):
    '''
    Funcion que dado un JSON con preguntas y respuestas (asumimos que las preguntas están en la clave 'question' del JSON, y las respuestas en 'verbalized_answers'), 
    una url a través de la cual realizar consultas y un csv donde guardar los resultados, hace una serie de metricas:
    - Realiza las preguntas del JSON dado
    - Lo compara con la respuesta esperada y obtiene varias metricas de rendimiento (Distancia de Levenshtein, BLEU, EM,...)
    - Guarda en el CSV la pregunta, la respuesta esperada, la respuesta obtenida y estas metricas
    '''
    VQuandaData = jsonToDict(JSONroute)

    with open(csvRoute,'w', newline='', encoding="utf-8") as f:

        csvwriter = csv.writer(f,delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)

        #Escribimos el Header
        csvwriter.writerow( ["Question", "Answer", "Response", "Levenshtein Distance","BLEU Score","EM Score","Query Time","Text Length","Is Answered"])

        for i in VQuandaData:
            pool.apply_async(evaluateQuestion(i,queryURL,csvwriter))
        pool.close()
        pool.join()
        f.close()

if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())
    queryUrl = "http://localhost:5000/eqakg/dbpedia/en?text=false"
    #queryUrl = "https://librairy.linkeddata.es/eqakg/dbpedia/en?text=false" 
    EQAKGMetrics(pool,"test.json",queryUrl,"results/VQuanda.csv")