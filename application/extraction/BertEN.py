# -*- coding: utf-8 -*-
from transformers import pipeline


class BertEN:
    
    def __init__(self):
        print("Loading bert-large-uncased-whole-word-masking-finetuned-squad model..")
        self.question_answerer = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad", tokenizer="bert-large-uncased-whole-word-masking-finetuned-squad")
        print("model ready")
        
    def get_answer(self,question,context):
        result = self.question_answerer(question=question, context=context, min_answer_len=1, max_answer_len=100)
        print(f"Answer: '{result['answer']}', score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']}")
        response = {}
        response['value']=result['answer']
        response['score']=round(result['score'], 4)
        return response