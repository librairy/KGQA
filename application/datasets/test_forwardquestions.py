from application.app import app

import application.summary.kg.wikidata.Wikidata as summary
import application.extraction as extraction
import application.response as response
import application.workflow as wf

import requests, json, os
import warnings
warnings.filterwarnings("ignore")
import jsonlines
from multiprocessing import Pool
from datetime import datetime
from timeit import default_timer as timer
import pywikibot

class ForwardQuestionsDataset:

    def __init__(self,workflow,input_file="data/all_questions.json"):
        print("reading test file:",input_file)
        with open(input_file,'r') as json_file:
         data = json.load(json_file)
        self.questions=data['questions']
        print("#Questions:", len(self.questions))
        self.workflow=workflow
        self.site = pywikibot.Site("wikidata", "wikidata")
        self.repo = site.data_repository()

    def is_valid(question_info):
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

    def do_question(question_info,use_entities=False):
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
      response = self.workflow.process(input_data)
      end = timer()
      result = {
          'ref_question':ref_question,
          'ref_answers':ref_answers,
          'answer': str(response['answer']),
          'confidence': response['confidence'],
          'evidence': response['evidence'],
          'time': end-start
      }
      return result

    def test(self,file_name=None,limit=10,use_entities=False,get_evidence=False,pool_size=1):

        if (file_name is None):
            file_id = "_".join([kb, str(int(use_entities)), str(int(get_evidence)), str(limit)])
            file_name = "result-"+file_id+".json"
        print("Output file:",file_name)

        pool = Pool(pool_size)

        with open(file_name, 'w') as json_writer:

         incr = pool_size
         min = 0
         max = incr

         #total = len(questions)
         total = len(self.questions)
         if (limit > 0):
             total = limit

         while(min < total):
          responses = pool.map(self.do_question, self.questions[min:max])
          print("[",datetime.now(),"]",min,":",max,"/",total)
          for response in responses:
           json_record = json.dumps(response, ensure_ascii=False)
           json_writer.write(json_record+"\n")
          min = max
          max += incr
         print("test ended")


if __name__ == '__main__':

    wikidataEN = summary.kg.wikidata.WikidataEN()
    extractive_bertEN = extraction.BertEN()
    response_EN = response.BertAnswererEN()
    workflow = wf.Workflow([wikidataEN],extractive_bertEN,response_EN)

    fqd = ForwardQuestionsDataset(workflow)
    fqd.test("out-1.json",1,True)
