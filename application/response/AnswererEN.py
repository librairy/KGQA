#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 12:05:15 2021

@author: cbadenes
"""

import application.response.BertENClassifier as classifier

class AnswererEN:
    
    def __init__(self):
        self.classifier = classifier.BertQuestionClassifier("./resources_dir")
        print("English answerer is ready")
        
        
    def get_response(self, question, answer):
        category = self.classifier.get_category(question)
        print("Category:",category['category'])
        print("Type:",category['type'])
        response = answer
        response2 = ""
        if (category['category'] == 'boolean'):
            if not answer:
                response2 = "None"
                response = "False"
            else:
                response2 = answer
                response = "True"
        elif (len(category['type']) > 0) and (category['type'][0] == 'number'):
            if not answer:
                response2 = "None"
                response = str(0)
            else:
                if not ((answer.replace('.', '', 1)).isdigit()):
                    response2 = answer
                    response = str(len(answer.split(",")))
        return [response,response2]       
        