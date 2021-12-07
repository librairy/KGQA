import json
import re
import csv
import pandas

def nthOfChar(string, char, n):
    '''
    Funcion auxiliar que extrae un substring hasta el n-esimo caracter
    '''
    regex=r'^((?:[^%c]*%c){%d}[^%c]*)%c(.*)' % (char,char,n-1,char,char)
    regexGroups = re.match(regex, string)
    if regexGroups is not None:
        return regexGroups.group(1)
    else:
        return ""

def jsonToDict(route) -> dict:
    '''
    Funcion auxiliar que dada la ruta de un json, lo abre y lo convierte a diccionario
    '''
    with open(route, encoding="utf-8") as f:
        return json.load(f)

def questionNotInCsv(JSONroute, csvRoute):
    '''
    Funcion auxiliar que dado un csv y un json con preguntas y respuestas, ve que preguntas no estan en el csv. 
    Es utilizado para ver que preguntas no estan siendo ver respondidas por el sistema.
    '''
    VQuandaData = jsonToDict(JSONroute)

    with open('exceptionQuestions.csv','w', newline='', encoding="utf-8") as f:

        firstColumnValues = ((pandas.read_csv(csvRoute,sep=';')).iloc[:, 0]).unique()

        csvwriter = csv.writer(f,delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)   
        csvwriter.writerow(["Question","Answer","Is Answered"])     
        for i in VQuandaData:
            if i['question'] not in firstColumnValues:
                isAnswered = "YES"
                modelAnswerLongGroups = re.search(r"\[([^\)]+)\]", i['verbalized_answer'])
                if(modelAnswerLongGroups is not None):
                    modelAnswer = modelAnswerLongGroups.group(1)
                else:
                    modelAnswer = "None"
                    isAnswered = "NO"
                csvwriter.writerow([i['question'], modelAnswer, isAnswered])
    
    f.close()

questionNotInCsv("test.json","results/VQuanda.csv")