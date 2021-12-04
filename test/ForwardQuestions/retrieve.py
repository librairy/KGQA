#!pip install sacrebleu
#!pip install -U nltk

import requests, json
import warnings
warnings.filterwarnings("ignore")
from sacrebleu import sentence_bleu
import nltk
import csv
from multiprocessing import Pool
from datetime import datetime
from timeit import default_timer as timer
import nltk
nltk.download('wordnet')




def exactMatchScore(string1,string2):
    '''
    Funcion auxiliar que incorpora la medida EM (Exact Match). 1 si ambas cadenas son iguales, 0 e.o.c.
    Para listas de cadenas, comprueba si ambas contienen los mismos elementos (no importa el orden)
    '''
    if ("," in string1) and ("," in string2):
        string1 = string1.split(",")
        string2 = string2.split(",")
        return int((len(string1) == len(string2)) and (set(string1) == set(string2)))
    return int(string1 == string2)


def do_question(question_info):
  start = timer()
  question_txt = question_info['question']+"?"
  if (len(question_info['answers']) < 1 ):
    print("EMPTY answer")
    return {}
  answer_txt = ",".join(question_info['answers']).lower()
  print("->",question_txt, answer_txt)
  response = requests.get("http://127.0.0.1:5000/eqakg/dbpedia/en", params={ 'text': True}, data={'question':question_txt})
  if (response.status_code != 200):
    print("ERROR",response)
    return {}
  response_json = response.json()
  end = timer()
  response_txt = str(response_json['answer']).lower()
  result = {
      'question':question_txt,
      'answer':answer_txt,
      'response': response_txt,
      'levenshtein': nltk.edit_distance(answer_txt, response_txt),
      'sacre_bleu': sentence_bleu(response_txt,answer_txt.split(" ")).score,
      'bleu': nltk.translate.bleu_score.sentence_bleu([answer_txt.split(" ")], response_txt.split(" ")),
      'meteor': nltk.translate.meteor_score.single_meteor_score(answer_txt.split(" "), response_txt.split(" ")),
      'em': exactMatchScore(answer_txt,response_txt),
      'time': end-start,
      'length': len(response_txt),
      'answered': len(answer_txt)>0,
      'text': response_json['text']
  }
  print("<-",result)
  return result



fq_dataset = {
    'olympic_games': "https://raw.githubusercontent.com/johannamelly/ForwardQuestions/master/questions/olympic_games.json",
    'politics_of_the_united_states': "https://raw.githubusercontent.com/johannamelly/ForwardQuestions/master/questions/politics_of_the_united_states.json",
    'rock_music':"https://raw.githubusercontent.com/johannamelly/ForwardQuestions/master/questions/rock_music.json",
    'super_mario_bros':"https://raw.githubusercontent.com/johannamelly/ForwardQuestions/master/questions/super_mario_bros.json",
    'switzerland':"https://raw.githubusercontent.com/johannamelly/ForwardQuestions/master/questions/switzerland.json",
    'the_legend_of_zelda':"https://raw.githubusercontent.com/johannamelly/ForwardQuestions/master/questions/the_legend_of_zelda.json",
    'world_war_2':"https://raw.githubusercontent.com/johannamelly/ForwardQuestions/master/questions/world_war_2.json"
}


# field names 
csv_fields = ['Question','Answer','Response','Levenshtein Distance','BLEU Score (SacreBleu)','BLEU Score (ntlk)','Meteor Score','EM Score','Query Time','Text Length','Is Answered','Text']

        
if __name__ == '__main__':
 
 for key in fq_dataset:
     pool_size = 4    
     pool = Pool(pool_size)
     data = requests.get(fq_dataset[key])
     data_json = json.loads(data.text)
     questions = data_json['questions']
     print(len(questions),"questions in",key,"dataset")

     # name of csv file 
     filename = key+".csv"

     # writing to csv file 
     with open(filename, 'w') as csvfile:
      csvwriter = csv.writer(csvfile) 
      # writing the fields 
      csvwriter.writerow(csv_fields) 

      # writing the data rows 
      #csvwriter.writerows(rows)

      min = 0
      max = 0
      incr = pool_size
      counter = 0    

      while(max < len(questions)):
       min = counter
       max = min + incr
       if (max > len(questions)):
        max = len(questions)
       responses = pool.map(do_question, questions[min:max])
       print("[",datetime.now(),"]","writing",len(responses)," responses...")
       try:
        rows = [ [result['question'],result['answer'],result['response'],result['levenshtein'],result['sacre_bleu'],result['bleu'],result['meteor'],result['em'],result['time'],result['length'],result['answered'],result['text']] for result in responses if len(result)>0 ]
        csvwriter.writerows(rows)
       except e:
        print("Write error. Wait for 5secs..",e)        
       counter=max


