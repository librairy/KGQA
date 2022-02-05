from pandas import pd

def csvToDict(route) -> dict:
    '''
    Funcion auxiliar que dada la ruta de un csv, lo abre y lo convierte a lista de diccionarios
    '''
    df = pd.read_csv(route, sep=";")
    return df.to_dict('records')

def findValueIndex(dictList, key, value):
    '''
    Funcion auxiliar que dada una lista de diccionarios y un valor de este,
    encuentra en qué diccionario está dicho valor
    '''  
    for i, dict in enumerate(dictList):
        if dict[key] == value:
            return i
    return -1

def extractLatestQuestionCSV(csvRoute):
    df = pd.read_csv(csvRoute, sep=";")
    return df.iloc[-1,0]


dictList = csvToDict("LC-Quad_Dataset.csv")
#pprint(dictList)
#print(len(dictList))
#dictList[:] = [value for counter, value in enumerate(dictList) if counter > 10635]
#print(len(dictList))
question = extractLatestQuestionCSV("LC-Quad.csv")
#print(question)

print("Index:", findValueIndex(dictList, 'question', question))