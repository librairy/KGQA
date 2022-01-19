import requests, json, os
import warnings
warnings.filterwarnings("ignore")
import jsonlines
from multiprocessing import Pool
from datetime import datetime
from timeit import default_timer as timer

##############################################################
# Test Parameters
input_file      = "data/available_questions.json"
output_file     = "results/available_questions_all.json"
endpoint        = "muheqa/all/en"
use_entities    = False
use_evidence    = True
###############################################################

def do_question(question_info):
  start = timer()
  ref_question = question_info['question']
  if (not ref_question.endswith("?")):
      ref_question += "?"
  ref_answers = question_info['object']
  input_data = {'question':ref_question}
  entities=""
  if (use_entities):
      entity_id = question_info['subjectCode']
      entity_name = question_info['subjet']
      input_data['entities']=entity_id+";"+entity_name
  response = requests.get("http://127.0.0.1:5000/"+endpoint, params={ 'evidence': use_evidence}, data=input_data)
  if (response.status_code != 200):
    print("QUERY ERROR:",ref_question, " <- response:", response.text)
    return {}
  response_json = response.json()
  end = timer()
  result = {
      'ref_question':ref_question,
      'ref_answers':ref_answers,
      'answer': str(response_json['answer']),
      'score': response_json['score'],
      'evidence': response_json['evidence'],
      'time': end-start
  }
  return result


if __name__ == '__main__':

 print("reading file",input_file,"..")
 with open(input_file,'r') as json_file:
  data = json.load(json_file)

 pool_size = 1
 pool = Pool(pool_size)
 questions = data['questions']
 print(file, ":",len(questions),"questions")

 with open(output_file, 'w') as json_writer:

  incr = pool_size
  min = 0
  max = incr

  total = len(questions)

  while(min < total):
   responses = pool.map(do_question, questions[min:max])
   print("[",datetime.now(),"]",min,":",max,"/",total)
   for response in responses:
    json_record = json.dumps(response, ensure_ascii=False)
    json_writer.write(json_record+"\n")
   min = max
   max += incr
  print("test ended")
