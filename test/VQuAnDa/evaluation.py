import csv
from sacrebleu import sentence_bleu
import pandas as pd
import nltk
from sklearn.metrics.pairwise import cosine_similarity

def csvToDict(route) -> dict:
    '''
    Funcion auxiliar que dada la ruta de un csv, lo abre y lo convierte a lista de diccionarios
    '''
    df = pd.read_csv(route, sep=";", na_filter=False)
    return df.to_dict('records')

def exactMatchScore(string1,string2):
    '''
    Funcion auxiliar que incorpora la medida EM (Exact Match). 1 si ambas cadenas son iguales, 0 e.o.c.
    Para listas de cadenas, comprueba si ambas contienen los mismos elementos (no importa el orden)
    '''
    if ("," in string1) and ("," in string2):
        string1 = string1.split(", ")
        string2 = string2.split(", ")
        return int((len(string1) == len(string2)) and (set(string1) == set(string2)))
    return int(string1 == string2)

def evaluateQuestion(questionDict):
    '''
    Funcion auxiliar que calcula las metricas para una determinada pregunta y las escribe en un CSV en una ruta dada..
    '''
    modelAnswer = questionDict['Answer']
    obtainedAnswer = questionDict['Response']
    if obtainedAnswer == "true":
        obtainedAnswer = "yes"  
    elif obtainedAnswer == "false":
        obtainedAnswer = "no"

    sacreBleuScore = sentence_bleu(obtainedAnswer,[modelAnswer]).score
    bleuScore = nltk.translate.bleu_score.sentence_bleu([modelAnswer], obtainedAnswer)*100
    meteorScore = nltk.translate.meteor_score.meteor_score([[modelAnswer]],[obtainedAnswer])*100
    
    global rows
    rows.append( [questionDict['Question'], sacreBleuScore, bleuScore, meteorScore, exactMatchScore(modelAnswer,obtainedAnswer),"placeholder"] )

def evaluator(csvRoute1, csvRoute2, writeHeader = False):
    '''
    Funcion que dado un csv con preguntas, las respuestas obtenidas y las respuestas modelo, hace una serie de metricas (BLEU, EM, METEOR,...)
    '''
    data = csvToDict(csvRoute1)
    
    #Escribimos el Header
    if writeHeader:
        with open(csvRoute2,'w', newline='', encoding="utf-8") as f:
            csvwriter = csv.writer(f,delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            csvwriter.writerow(header)
            f.close()
        
    for value,i in enumerate(data):
        evaluateQuestion(i)
        if value != 0 and value % 24 == 0:
            with open(csvRoute2, 'a', newline='', encoding="utf-8") as f:
                global rows
                (pd.DataFrame.from_records(rows, columns=header)).to_csv(f, header=False, index=False, sep=';', quoting=csv.QUOTE_ALL)
                rows[:] = []
                f.close()

    #Escribimos lo que quede
    with open(csvRoute2, 'a', newline='', encoding="utf-8") as f:
        (pd.DataFrame.from_records(rows, columns=header)).to_csv(f,header=False, index=False, sep=';', quoting=csv.QUOTE_ALL)
        f.close()

rows = []
header = ["Question","SacreBLEU","BLEU","Meteor","EM","Cosine Similarity"]

evaluator("results/VQuAnDa.csv","results/VQuAnDa_Evaluation.csv", writeHeader=True)