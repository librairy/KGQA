import pandas as pd
import json
from pprint import pprint


def JSONLineToDict(JSONRoute):
    '''
    Funcion auxiliar que dado un archivo json con JSONObjects en cada linea,
    lo abre y lo convierte a lista de diccionarios
    '''  
    with open(JSONRoute) as f:
        jsonList = list(f)
    
    return json.loads(json.dumps([json.loads(jsonLine) for jsonLine in jsonList]))


def findValueIndex(dictList, key, value):
    '''
    Funcion auxiliar que dada una lista de diccionarios y un valor de este,
    encuentra en qué diccionario está dicho valor
    '''  
    for i, dict in enumerate(dictList):
        if dict[key] == value:
            return i
    return -1

dictList = JSONLineToDict("Vanilla_Dataset_Test.json")
print(len(dictList))


dictList[:] = [value for counter, value in enumerate(dictList) if counter >= 1000 and counter < 2000]
print(len(dictList))

for i in dictList:
    print(i['question'])

#pprint(JSONLineToDict("Vanilla_Dataset_Test.json","test.json"))

