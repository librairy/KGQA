import csv
import json
import pandas as pd
import google_auth_oauthlib
from pprint import pprint
import re

def jsonToDict(route):
    '''
    Funcion auxiliar que dada la ruta de un json, lo abre y lo convierte a lista de diccionarios
    '''
    with open(route, encoding="utf-8") as f:
        return json.load(f)

def JSONLineToDict(JSONRoute):
    '''
    Funcion auxiliar que dado un archivo json con JSONObjects en cada linea,
    lo abre y lo convierte a lista de diccionarios
    '''  
    with open(JSONRoute) as f:
        jsonList = list(f)
    
    return json.loads(json.dumps([json.loads(jsonLine) for jsonLine in jsonList]))

def csvToDict(route):
    '''
    Funcion auxiliar que dada la ruta de un csv, lo abre y lo convierte a lista de diccionarios
    '''
    df = pd.read_csv(route, sep=";")
    return df.to_dict('records')

def parseDataset(dataset):
    """
    Funcion que abre datasets, los limpia y guarda como CSV
    """
    datasetRoute = "test/datasets/" + dataset + "/data/"
    if dataset == "VQuAnDa":
        #Cargamos dataset como dataframe
        dataset = jsonToDict(datasetRoute + "test.json")
        df = pd.DataFrame(dataset)

        df.drop(columns=["query"],inplace=True)
        s = pd.Series(df["verbalized_answer"])
        s = s.apply(lambda st: st[st.find("[")+1:st.find("]")])
        df["verbalized_answer"] = s.to_frame()
        df.rename(columns={"verbalized_answer":"answer", "uid":"question_id"},inplace=True)

    elif dataset == "VANiLLA":
        #Cargamos dataset como dataframe
        dataset = JSONLineToDict(datasetRoute + "Vanilla_Dataset_Test.json")
        df = pd.DataFrame(dataset)

        df.drop(columns=["answer_sentence","question_entity_label","question_relation"],inplace=True)

    elif dataset == "LC-QuAD_2.0":
        #Cargamos dataset como dataframe
        df = pd.read_csv(datasetRoute + "LC-Quad_Dataset.csv", sep=";")
        df = df.fillna("")

        df.drop(columns=["Query","QIDs"],inplace=True)
        df.rename(columns={"Entities/Answer":"answer", "Question":"question"},inplace=True)
        df['question_id'] = range(0, len(df))
    
    df.drop_duplicates(subset=["question"],keep="first",inplace=True)
    df = df[["question_id","question","answer"]]
    df.to_csv(datasetRoute + "parsedDataset.csv", sep = ";", quoting=csv.QUOTE_ALL, index=False)


#Ejecutamos parseDataset para nuestros datasets
datasets = ["VANiLLA","VQuAnDa","LC-QuAD_2.0"]
for i in datasets:
    parseDataset(i)