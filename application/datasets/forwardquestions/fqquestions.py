import json, os
import warnings
warnings.filterwarnings("ignore")
import jsonlines
#from multiprocessing import Pool
from datetime import datetime
from timeit import default_timer as timer
from functools import partial
from itertools import repeat
from multiprocessing import Pool, freeze_support

class ForwardQuestions:

    def __init__(self,input_file="data/questions/olympic_games.json"):
        print("Input file:",input_file)
        with open(input_file,'r') as json_file:
         data = json.load(json_file)
        self.questions=data['questions']
        print("number of questions:", len(self.questions))

    def do_question(self,question_info,use_entities,workflow):
      start = timer()
      ref_question = question_info['question']
      if (not ref_question.endswith("?")):
          ref_question += "?"
      ref_answers = question_info['answers']
      input_data = {'question':ref_question}
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
              responses.append(self.do_question(question,use_entities,workflow))
          print("[",datetime.now(),"]",min,":",max,"/",total)
          for response in responses:
           json_record = json.dumps(response, ensure_ascii=False)
           json_writer.write(json_record+"\n")
          min = max
          max += incr
         print("test ended")
         return count
