from flask import Flask, request, abort, jsonify, send_from_directory#, session,
from logging.handlers import RotatingFileHandler
from application import config
from flask_cors import CORS

import application.summary.DBpediaEN as dbpedia_en
import application.summary.DBpediaES as dbpedia_es
import application.summary.WikidataEN as wikidata_en
import application.summary.WikidataES as wikidata_es
import application.summary.Cord19EN as cord19_en
import application.extraction.BertEN as bert_en
import application.extraction.RobertaCovidEN as roberta_covid_en
import application.extraction.RobertaEN as roberta_en
import application.response.AnswererEN as answerer_en
import json

class Workflow:

    def __init__(self):
        print("MuHeQA workflow ready")

    def decapitalize(self,str):
        return str[:1].lower() + str[1:]


    def process(self,request,summarizer_list,extractive_qa,response_builder):
        question = request['question']
        print("Making question:",question,"..")


        entity_list = []
        if 'entities' in request:
            print("input entities:",request['entities'])
            for e in request['entities'].split("#"):
                values = e.split(";")
                entity_list.append({ 'id': values[0], 'name': values[1]})


        req_evidence = False
        if ('evidence' in request):
            req_evidence = request['evidence']

        # Compose Summary
        question = self.decapitalize(question)
        summary = ""
        for summarizer in summarizer_list:
            partial_summary = ""
            if (len(entity_list)==0):
                partial_summary = summarizer.get_summary(question)
            else:
                partial_summary = summarizer.get_summary_from_entities(question,entity_list)
            summary += partial_summary + " "

        # Extract Answer
        answer = extractive_qa.get_answer(question,summary)

        # Create Reponse
        value = response_builder.get_response(question, answer['value'])

        # Return value
        response = {}
        response['question'] = question
        response['answer'] = value[0]
        response['confidence'] = answer['score']
        response['result'] = value[1]
        if req_evidence.lower() == 'true':
            response['evidence'] = answer['summary']

        print("Response: ", response['answer'])

        return response
