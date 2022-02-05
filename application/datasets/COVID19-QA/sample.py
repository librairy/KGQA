import json
import warnings
warnings.filterwarnings("ignore")
from datetime import datetime
from timeit import default_timer as timer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sys
import collections

if (len(sys.argv) < 3):
    print("Type filename to be evaluated (e.g. python evaluate.py input.json)")
    sys.exit(2)


if __name__ == '__main__':

 input_file_1 = open(sys.argv[1],'r')
 input_file_2 = open(sys.argv[2],'r')

 filter = None
 if (len(sys.argv) > 3):
     filter = sys.argv[3]
     print("Filter:",filter)

 count = 0
 while True:
     count +=1
     line1 = input_file_1.readline()
     line2 = input_file_2.readline()
     if not line1 or not line2:
         break
     json_line1 = json.loads(line1)
     json_line2 = json.loads(line2)
     if (len(json_line1) == 0) or (len(json_line2) == 0):
         continue
     q1 = json_line1['ref_question']
     ref_answer = json_line1['ref_answers'][0]
     answer1 = json_line1['answer']
     answer2 = json_line2['answer']
     if (answer1 == None) or (answer1 == None):
         continue
     if (filter != None):
         q_type = q.lower().split(" ")[0]
         q_types.append(q_type)
         if (q_type != filter.lower()):
             continue
     if (ref_answer == answer1) and (answer1 != answer2):
        print("Line{}-{}: {} <-> {} / {}".format(count, q1, ref_answer, answer1, answer2))

 if (filter != None):
     counter=collections.Counter(q_types)
     print(counter)
