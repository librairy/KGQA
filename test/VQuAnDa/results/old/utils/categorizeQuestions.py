import csv
from utils import jsonToDict
from utils import nthOfChar

def extractNthWords(jsonRoute, questionList, n):
    '''
    Funcion auxiliar que escribe en un .csv la pregunta, sus n primeras palabras y sus n ultimas palabras
    '''
    VQuandaData = jsonToDict(jsonRoute)
    with open(questionList,'w', newline='', encoding="utf-8") as f:
        csvwriter = csv.writer(f,delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        csvwriter.writerow(["Question","First " + str(n) + " Words","Last " + str(n) + " Words"])
        for i in VQuandaData:
            question = i['question']
            csvwriter.writerow([question,nthOfChar(question," ",3),question.replace(nthOfChar(question," ",(question.count(' ') - 2)),"")])
    f.close()

extractNthWords("train.JSON","questionList.csv", 3)