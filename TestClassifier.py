#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 11:43:45 2021

@author: cbadenes

question_label = "list"
if question_type == 2:
    question_label = "count"
elif question_type == 1:
    question_label = "ask"
    
"""
import application.question.Classifier as classifier
import application.question.LinearClassifier as linear_classifier
import application.question.BertbasedClassifier as bert_classifier


question_type_classifier = classifier.Classifier("./application/question/svm.model")
linear_question_type_classifier = linear_classifier.TRECClassifier()
bert_classifier = bert_classifier.BertQuestionClassifier("/Users/cbadenes/Projects/isl-smart-task/resources_dir")

questions = [
    "Which universities are alma mater to Charles Plosser?",
    "Name the basketball player who played for Phoenix Suns and Los Angeles Clippers was his draft team?",
    "Count the key people of the Clinton Foundation?",
    "What is the purpose of Maharashtra Chess Association ?",
    "Tandem Computers is the subsidiary of which company?",
    "List all the collaborators of the artist which has collaborated with sanremo Music Festival?",
    "Was Noko a band member of Luxuria?",
    "How many other genre are there of the radio stations whose one of the genre is Classic rock?",
    "When was the first steel mill in the United States built ?",
    "CNN began broadcasting in what year ?"
    ]

for question in questions:
    print("question:",question)

    question_class = linear_question_type_classifier.get_category(question)
    print("linear classifier: {0}".format(question_class))
    
    question_type = question_type_classifier.predict([question])
    print("svm classifier:", question_type)
    
    answer_type = bert_classifier.get_category(question)
    print("BERT-based Class:", answer_type)
    


print(question_type)