import requests, json, os
import warnings
warnings.filterwarnings("ignore")
import jsonlines
from multiprocessing import Pool
from datetime import datetime
from timeit import default_timer as timer
import pywikibot


##############################################################
# Test Parameters
limit           = 33000
input_file      = "data/all_questions.json"
endpoint        = "muheqa/wikidata/en"
use_entities    = False
get_evidence    = True
###############################################################
test_name            = "_".join([endpoint.split("/")[1], str(int(use_entities)), str(int(get_evidence)), str(limit)])
output_file     = "results/bert/"+test_name+".json"

site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()

def is_valid(question_info):
    subject_code = question_info['subjectCode'].replace(" ","_")
    url = "https://www.wikidata.org/wiki/"+subject_code
    item = pywikibot.ItemPage(repo, subject_code)
    try:
        item_dict = item.get()
        print("Entity:", subject_code,"exists")
        return True
    except pywikibot.exceptions.IsRedirectPageError as e:
        print("Entity:",subject_code,"is redirected")
        return False
    except pywikibot.exceptions.NoPageError as e:
        print("Entity:",subject_code,"is missing")
        return False


def do_question(question_info):
  start = timer()
  ref_question = question_info['question']
  if (not is_valid(question_info)):
      return {}
  if (not ref_question.endswith("?")):
      ref_question += "?"
  ref_answers = question_info['object']
  input_data = {'question':ref_question}
  entities=""
  if (use_entities):
      entity_id = question_info['subjectCode']
      entity_name = question_info['subjet']
      input_data['entities']=entity_id+";"+entity_name
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
 questions = data['questions']
 print(input_file, ":",len(questions),"questions")

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
