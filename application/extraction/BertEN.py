# -*- coding: utf-8 -*-
from transformers import pipeline

class BertEN:
    
    def __init__(self):
        print("Loading bert-large-uncased-whole-word-masking-finetuned-squad model..")
        eqa_model = "bert-large-uncased-whole-word-masking-finetuned-squad"
        self.question_answerer = pipeline("question-answering", model=eqa_model, tokenizer=eqa_model)
        print("model ready")
        
    def chunks(self,lst,n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]    
        
    def get_answer(self,question,context):
        response = { "value":"", "score":0, "summary":""}
        sentences = [i for i in context.split(".") if len(i.split(" ")) < 50]
        
        #print("Sentences in Summary:", len(sentences))
        for chunk in self.chunks(sentences,10):
            #print("getting partial answer")    
            text = ". ".join(chunk)
            #print("num tokens:", len(text.split(" ")), "num_characters:", len(text))
            result = self.question_answerer(question=question, context=text, min_answer_len=1, max_answer_len=100)
            #print(f"Partial Answer: '{result['answer']}', score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']}")
            score = round(result['score'], 4)
            if (score > response['score']):
                response['value']=result['answer']
                response['score']=score
                response['summary']=text
        return response