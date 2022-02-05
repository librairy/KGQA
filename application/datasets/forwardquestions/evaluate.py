import json
import warnings
warnings.filterwarnings("ignore")
from datetime import datetime
from timeit import default_timer as timer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sys
import collections

if (len(sys.argv) < 2):
    print("Type filename to be evaluated (e.g. python evaluate.py input.json)")
    sys.exit(2)

# https://www.sbert.net/docs/pretrained_models.html
model_id='bert-base-nli-mean-tokens'
print("loading model",model_id,"..")
model = SentenceTransformer(model_id)

def get_text_similarity(string1,string2):
    sen = [
        string1,
        string2
    ]

    sen_embeddings = model.encode(sen)

    #let's calculate cosine similarity for sentence 0:
    result = cosine_similarity(
        [sen_embeddings[0]],sen_embeddings[1:]
    )
    return result[0][0]

def get_exactMatch_score(string1,string2):
    s1 = string1.lower().strip()
    s2 = string2.lower().strip()
    return int(s1 == s2)

def get_partialMatch_score(string1,string2):
    s1 = string1.lower().strip().split(" ")
    s2 = string2.lower().strip().split(" ")
    partial=False
    for e in s1:
        if (e in s2):
            partial=True
    return int(partial)

def get_fMeasure_score(string1,string2):
    s1 = string1.lower().strip()
    s2 = string2.lower().strip()
    ref = s1.split(" ")
    res = s2.split(" ")
    result = { 'tp':0.0, 'tn':0.0, 'fp':0.0, 'fn':0.0, 'precision':0.0, 'recall':0.0, 'f1':0.0}
    for e in res:
        if (e in ref):
            result['tp'] += 1.0
        else:
            result['fp'] += 1.0
    for x in ref:
        if (x not in res):
            result['fn'] += 1.0
    result['precision'] = result['tp'] /(result['tp'] + result['fp'])
    result['recall'] = result['tp'] /(result['tp'] + result['fn'])
    if (result['precision'] != 0.0) or (result['recall'] != 0.0):
        result['f1'] = (2*result['precision']*result['recall'])/(result['precision']+result['recall'])
    else:
        result['f1'] = 0.0
    return result


if __name__ == '__main__':

 input_file = sys.argv[1]
 filter = None
 if (len(sys.argv) > 2):
     filter = sys.argv[2]
     print("Filter:",filter)

 file = open(input_file,'r')
 count = 0
 em_results = []
 pm_results = []
 fmeasure_results = []
 ts_results = []
 q_types = []
 while True:
     count +=1
     line = file.readline()
     if not line:
         break
     json_line = json.loads(line)
     if (len(json_line) == 0):
         continue
     q = json_line['ref_question']
     s1 = json_line['ref_answers']
     s2 = json_line['answer']
     if (s1 == None) or (s2 == None):
         continue
     if (filter != None):
         q_type = q.lower().split(" ")[0]
         q_types.append(q_type)
         if (q_type != filter.lower()):
             continue
     print("Line{}: {} <-> {}".format(count, s1, s2))
     em_results.append(get_exactMatch_score(s1,s2))
     pm_results.append(get_partialMatch_score(s1,s2))
     fmeasure_results.append(get_fMeasure_score(s1,s2))
     ts_results.append(get_text_similarity(s1,s2))

 print("Total:",len(em_results))
 print("ExactMatch: ", sum(em_results)/len(em_results))
 print("PartialMatch: ", sum(pm_results)/len(pm_results))
 f1_results = [ e['f1'] for e in fmeasure_results]
 print("Macro-Average: ", sum(f1_results)/len(f1_results))
 total_tp = sum([ e['tp'] for e in fmeasure_results])
 total_fp = sum([ e['fp'] for e in fmeasure_results])
 total_fn = sum([ e['fn'] for e in fmeasure_results])
 print("Micro-Average: ", total_tp/(total_tp+total_fp))
 print("TextSimilarity: ", sum(ts_results)/len(ts_results))
 if (filter != None):
     counter=collections.Counter(q_types)
     print(counter)
