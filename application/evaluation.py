import json
import warnings
warnings.filterwarnings("ignore")
from datetime import datetime
from timeit import default_timer as timer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sys
import collections


class Evaluation:

    def __init__(self,similarity_model='bert-base-nli-mean-tokens'):
        # https://www.sbert.net/docs/pretrained_models.html
        print("loading model",similarity_model,"..")
        self.model = SentenceTransformer(similarity_model)

    def get_text_similarity(self,string1,string2):
        text = [
            string1,
            string2
        ]

        embeddings = self.model.encode(text)

        #let's calculate cosine similarity for sentence 0:
        result = cosine_similarity(
            [embeddings[0]],embeddings[1:]
        )
        return result[0][0]

    def get_exactMatch_score(self,string1,string2):
        s1 = string1.lower().strip()
        s2 = string2.lower().strip()
        return int(s1 == s2)

    def get_partialMatch_score(self,string1,string2):
        s1 = string1.lower().strip().split(" ")
        s2 = string2.lower().strip().split(" ")
        partial=False
        for e in s1:
            if (e in s2):
                partial=True
        return int(partial)

    def get_fMeasure_score(self,string1,string2):
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

    def run(self,input_file,filter=None):

         print("Evaluation: file=",input_file,", filter:",filter)

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
             if (s1 == None) or (q == None):
                 continue
             if (len(s1[0]) == 1):
                 s1 = [json_line['ref_answers']]
             s2 = json_line['answer']
             if (filter != None):
                 q_type = q.lower().split(" ")[0]
                 q_types.append(q_type)
                 if (q_type != filter.lower()):
                     continue
             print("Line{}: {} <-> {}".format(count, s1, s2))
             best_em = 0.0
             best_pm = 0.0
             best_f1 = {'f1':0.0}
             best_ts = 0.0
             for s1_candidate in s1:
                 p_score = self.get_exactMatch_score(s1_candidate,s2)
                 if (p_score >= best_em):
                     best_em = p_score
                 p_score = self.get_partialMatch_score(s1_candidate,s2)
                 if (p_score >= best_pm):
                     best_pm = p_score
                 p_score = self.get_fMeasure_score(s1_candidate,s2)
                 if (p_score['f1'] >= best_f1['f1']):
                     best_f1 = p_score
                 p_score = self.get_text_similarity(s1_candidate,s2)
                 if (p_score >= best_ts):
                     best_ts = p_score

             em_results.append(best_em)
             pm_results.append(best_pm)
             fmeasure_results.append(best_f1)
             ts_results.append(best_ts)

         result = {}
         result['total']= len(em_results)
         result["exact-match"]= 0.0
         if (len(em_results) > 0):
             result['exact-match'] = sum(em_results)/len(em_results)
         result["partial-match"]=0.0
         if (len(pm_results) > 0):
             result["partial-match"]=sum(pm_results)/len(pm_results)
         f1_results = [ e['f1'] for e in fmeasure_results]
         result["macro-average"]=0.0
         if (len(f1_results) > 0):
             result['macro-average'] = sum(f1_results)/len(f1_results)
         total_tp = sum([ e['tp'] for e in fmeasure_results])
         result['tp']=total_tp
         total_fp = sum([ e['fp'] for e in fmeasure_results])
         result['fp']=total_fp
         total_fn = sum([ e['fn'] for e in fmeasure_results])
         result['fn']=total_fn
         result['micro-average']=0.0
         if (total_tp+total_fp != 0.0):
             result['micro-average']=total_tp/(total_tp+total_fp)
         result['text-similarity']=0.0
         if (len(ts_results) > 0):
             result['text-similarity']=sum(ts_results)/len(ts_results)
         if (filter != None):
             counter=collections.Counter(q_types)
             result['filtered']= counter
             result['filter']=filter
         print(result)
         return result
