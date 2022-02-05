#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 12:05:15 2021

@author: cbadenes
"""

import application.response.BertENClassifier as classifier
import application.response.Answerer as answerer

class BertAnswererEN(answerer.Answerer):

    def __init__(self):
        super().__init__()
        self.classifier = classifier.BertQuestionClassifier("./resources_dir")
        print("English answerer is ready")


    def get_response(self, question, evidence):
        category = self.classifier.get_category(question)
        print("Category:",category['category'],"Evidence:",evidence)
        #print("Type:",category['type'])
        answer = None
        if (category['category'] == 'resource'):
            answer = evidence
        elif (category['category'] == 'boolean'):
            parts = question.lower().split(" ")
            if ('or' in parts):
                answer = evidence
            elif ('no' in parts) or ('false' in parts):
                answer = 'no'
            else:
                answer = 'yes'
        elif (len(category['type']) > 0) and (category['type'][0] == 'number'):
            if answer is None:
                answer = str(0)
            elif not ((answer.replace('.', '', 1)).isdigit()):
                answer = str(len(answer.split(",")))
        return answer
