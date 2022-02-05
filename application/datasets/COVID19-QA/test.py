import requests, json, os
import warnings
warnings.filterwarnings("ignore")
import jsonlines
from multiprocessing import Pool
from datetime import datetime
from timeit import default_timer as timer


##############################################################
# Test Parameters
limit           = 100
input_file      = "data/COVID-QA.json"
endpoint        = "muheqa/all/en"
use_entities    = False
get_evidence    = True
###############################################################
test_name            = "_".join([endpoint.split("/")[1], str(int(use_entities)), str(int(get_evidence)), str(limit)])
output_file     = "results/bert-"+test_name+".json"

def is_valid(question_info):
    return not question_info['is_impossible']


def do_question(question_info):
  start = timer()
  ref_question = question_info['question']
  if (not is_valid(question_info)):
      return {}
  if (not ref_question.endswith("?")):
      ref_question += "?"
  ref_answers = []
  for answer in question_info['answers']:
      ref_answers.append(answer['text'])
  input_data = {'question':ref_question}

  response = requests.get("http://127.0.0.1:5000/"+endpoint, params={ 'evidence': get_evidence}, data=input_data)
  if (response.status_code != 200):
    print("QUERY ERROR:",ref_question, " <- response:", response.text)
    return {}
  response_json = response.json()
  end = timer()
  result = {
      'ref_question':ref_question,
      'ref_answers':ref_answers,
      'answer': str(response_json['answer']),
      'confidence': response_json['confidence'],
      'evidence': response_json['evidence'],
      'time': end-start
  }
  return result


if __name__ == '__main__':

 print("reading file",input_file," in test:", test_name,"..")
 with open(input_file,'r') as json_file:
  data = json.load(json_file)

 pool_size = 1
 pool = Pool(pool_size)
 questions = []
 papers = data['data']
 for paper in papers:
     paragraphs = paper['paragraphs']
     for paragraph in paragraphs:
         paragraph_questions = paragraph['qas']
         for question in paragraph_questions:
             questions.append(question)


 with open(output_file, 'w') as json_writer:

  incr = pool_size
  min = 0
  max = incr

  #total = len(questions)
  total = limit

  while(min < total):
   responses = pool.map(do_question, questions[min:max])
   print("[",datetime.now(),"]",min,":",max,"/",total)
   for response in responses:
    json_record = json.dumps(response, ensure_ascii=False)
    json_writer.write(json_record+"\n")
   min = max
   max += incr
  print("test ended")
