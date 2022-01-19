import requests, json, os
import warnings
warnings.filterwarnings("ignore")
import jsonlines
from multiprocessing import Pool
from datetime import datetime
from timeit import default_timer as timer

endpoint= "all"

def do_question(question_info):
  start = timer()
  ref_question = question_info['question']
  if (not ref_question.endswith("?")):
      ref_question += "?"
  ref_answers = question_info['object']
  response = requests.get("http://127.0.0.1:5000/muheqa/"+endpoint+"/en", params={ 'evidence': True}, data={'question':ref_question})
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

 filename = "all_questions.json"
 file = os.path.join("data", filename)
 print("reading file",file,"..")
 with open(file,'r') as json_file:
  data = json.load(json_file)
 print("start")

 pool_size = 1
 pool = Pool(pool_size)
 questions = data['questions']
 print(file, ":",len(questions),"questions")

 new_filename = filename.split(".")[0]+"_"+endpoint+"."+filename.split(".")[1]
 output_file = os.path.join("results", new_filename)
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
