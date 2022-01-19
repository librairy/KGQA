import requests,json, os
import warnings
warnings.filterwarnings("ignore")
import jsonlines
from datetime import datetime
from timeit import default_timer as timer
import pywikibot

if __name__ == '__main__':

 filename = "all_questions.json"
 file = os.path.join("data", filename)
 print("reading file",file,"..")
 with open(file,'r') as json_file:
  data = json.load(json_file)
 print("start")

 questions = data['questions']
 total_questions = len(questions)
 print(file, ":",total_questions,"questions")

 output_file = os.path.join("data", "available_questions.json")

 site = pywikibot.Site("wikidata", "wikidata")
 repo = site.data_repository()
 available_questions = []
 for question in questions:
    subject_code = question['subjectCode'].replace(" ","_")
    url = "https://www.wikidata.org/wiki/"+subject_code
    item = pywikibot.ItemPage(repo, subject_code)
    try:
        item_dict = item.get()
        print("Entity:", subject_code,"exists")
        available_questions.append(question)
    except pywikibot.exceptions.IsRedirectPageError as e:
        print("Entity:",subject_code,"is redirected")
    except pywikibot.exceptions.NoPageError as e:
        print("Entity:",subject_code,"is missing")

 print("Validation end.")
 print("Total Questions:", total_questions)
 total_available_questions = len(available_questions)
 print("Available Questions:", total_available_questions)
 print("Invalid Questions:", total_questions-total_available_questions)
 print("saving file...")
 with open(output_file, mode='w') as writer:
     result = { 'questions': available_questions}
     json.dump(result, writer)
 print("done!")
