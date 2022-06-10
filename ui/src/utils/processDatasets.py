import re
import os
import json
import pandas as pd

#Dataset fields we want to keep
keysToKeep = ["question","answer"]

def jsonToDict(file):
    '''
    Auxiliary function that converts a given a JSON file to dictionary list.
    '''
    return json.loads((file.read()).decode('utf-8'))

def jsonLineToDict(file):
    '''
    Auxiliary function that converts a given a JSON-Line file 
    (JSON Objects in each line) to dictionary list
    '''
    return json.loads(json.dumps([json.loads(jsonLine) for jsonLine in (file.read()).decode('utf-8').splitlines()]))

def csvToDict(file):
    '''
    Auxiliary function that converts a given a CSV file to dictionary list.
    '''
    df = pd.read_csv(file, sep=None, engine="python")
    #Convertimos los valores corruptos por cadenas vacias
    df = df.fillna("")
    return df.to_dict('records')

def formatDataset(file, isCsv = False, toDf = False):
    """
    Auxiliary function that formats a dataset and 
    returns it as CSV or Pandas Dataframe
    """
    #Convert csv or JSON to dictionary list
    if isCsv:
        dictList = csvToDict(file)
    else:
        try:
            dictList = jsonToDict(file)
        except:
            dictList = jsonLineToDict(file)
            
    #Retrieve question and answer for each dictionary        
    for i in dictList:
        #If answer is verbalized (between brackets), extract it with a regular expression
        if "verbalized_answer" in i.keys():
            answer = re.search(r"\[([^\)]+)\]", i["verbalized_answer"])
            if answer:
                i["verbalized_answer"] = answer.group(1)
            i["answer"] = i.pop("verbalized_answer")    
        keysToDelete = set(i.keys()).difference(keysToKeep)
        for k in keysToDelete:
            del i[k]
    
    #Delete repeated question and answers
    res = list({frozenset(item.items()) : item for item in dictList}.values())
    if toDf:
        return pd.DataFrame(res)
    return res