import json, os
import warnings
warnings.filterwarnings("ignore")
import jsonlines
#from multiprocessing import Pool
from datetime import datetime
from timeit import default_timer as timer
import pywikibot
from functools import partial
from itertools import repeat
from multiprocessing import Pool, freeze_support

class ForwardQuestionsDataset:

    def __init__(self,use_entities=False,input_file="data/all_questions.json"):
        print("Input file:",input_file)
        with open(input_file,'r') as json_file:
         data = json.load(json_file)
        self.use_entities = use_entities
        print("manual entities:", use_entities)
        self.questions=data['questions']
        print("number of questions:", len(self.questions))
        self.site = pywikibot.Site("wikidata", "wikidata")
        self.repo = self.site.data_repository()

    def is_valid(self,question_info):
        subject_code = question_info['subjectCode'].replace(" ","_")
        item = pywikibot.ItemPage(self.repo, subject_code)
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

    def do_question(self,question_info,workflow):
      start = timer()
      ref_question = question_info['question']
      if (not ref_question.endswith("?")):
          ref_question += "?"
      ref_answers = question_info['object']
      input_data = {'question':ref_question}
      entities=""
      if (self.use_entities):
          entity_id = question_info['subjectCode']
          entity_name = question_info['subjet']
          input_data['entities']=entity_id+";"+entity_name
      response = workflow.process(input_data)
      end = timer()
      result = {
          'ref_question':ref_question,
          'ref_answers':ref_answers,
          'answer': str(response['answer']),
          'confidence': response['confidence'],
          'time': end-start
      }
      if ('evidence' in response):
          result['evidence'] = response['evidence']
      return result

    def test(self,workflow,file_name=None,limit=10,use_entities=False,get_evidence=False,pool_size=1):

        if (file_name is None):
            file_id = "_".join([kb, str(int(use_entities)), str(int(get_evidence)), str(limit)])
            file_name = "result-"+file_id+".json"
        print("Output file:",file_name)

        #pool = Pool(pool_size)
        count = 0
        with open(file_name, 'w') as json_writer:

         incr = pool_size
         min = 0
         max = incr

         #total = len(questions)
         total = len(self.questions)
         if (limit > 0):
             total = limit

         while(min < total):
          #responses = pool.starmap(self.do_question, zip(self.questions[min:max], repeat(workflow)))
          responses = []
          for question in self.questions[min:max]:
              count += 1
              responses.append(self.do_question(question,workflow))
          print("[",datetime.now(),"]",min,":",max,"/",total)
          for response in responses:
           json_record = json.dumps(response, ensure_ascii=False)
           json_writer.write(json_record+"\n")
          min = max
          max += incr
         print("test ended")
         return count
