from flask import Flask, request, abort, jsonify, send_from_directory#, session,
from logging.handlers import RotatingFileHandler
from application import config
from flask_cors import CORS
from pprint import pprint

import application.summary.kg.dbpedia.DBpediaEN as dbpedia_en
import application.summary.kg.wikidata.WikidataEN as wikidata_en
import application.summary.txt.Cord19EN as cord19_en

import application.extraction.BertEQA as bert_eqa_en
import application.extraction.RobertaCovidEQA as roberta_covid_en
import application.extraction.RobertaEQA as roberta_en

import application.response.BertAnswererEN as response_en

import application.workflow as wf

app = Flask(__name__)
app.config.from_object(config)

cors = CORS(app)

dbpediaEN = dbpedia_en.DBpediaEN()
wikidataEN = wikidata_en.WikidataEN()
cord19EN = cord19_en.Cord19EN()

bertEQA = bert_eqa_en.BertEQA()
robertaCovidEQA = roberta_covid_en.RobertaCovidEQA()
robertaEQA = roberta_en.RobertaEQA()

bertRsp = response_en.BertAnswererEN()

@app.before_request
def before_request():
    app.logger.info('Request with question: %s for the uri %s .', request.method, request.path)


def handle_question(request,summarizer_list,extractive_qa,response_builder):
    question = request.form['question']
    if 'query' in request.args:
        question = request.args.get('question')
    if question is None:
        return jsonify({'error': 'question not received.'}), 400

    req = { 'question': question}

    if 'entities' in request.form:
        req['entities'] = request.form['entities']
    if 'entities' in request.args:
        req['entities'] = request.args.get('entities')

    if ('evidence' in request.args):
        req['evidence'] = request.args.get('evidence')

    workflow = wf.Workflow(summarizer_list,extractive_qa,response_builder)
    response = workflow.process(req)
    return jsonify(response), 200


## English DBpedia
@app.route('/muheqa/dbpedia/en', methods=['GET'])
@app.route('/muheqa/dbpedia', methods=['GET'])
def get_dbpedia_en():
    return handle_question(request, [dbpediaEN], bertEQA, bertRsp)

## Spanish DBpedia
@app.route('/muheqa/dbpedia/es', methods=['GET'])
def get_dbpedia_es():
    return handle_question(request, [dbpediaES], bertEQA, bertRsp)

## English Wikidata
@app.route('/muheqa/wikidata/en', methods=['GET'])
@app.route('/muheqa/wikidata', methods=['GET'])
def get_wikidata_en():
    return handle_question(request, [wikidataEN], bertEQA, bertRsp)

## Spanish Wikidata
@app.route('/muheqa/wikidata/es', methods=['GET'])
def get_wikidata_es():
    return handle_question(request, [wikidataES], bertEQA, bertRsp)

## English DBpedia
@app.route('/muheqa/cord19/en', methods=['GET'])
@app.route('/muheqa/cord19', methods=['GET'])
def get_cord19_en():
    return handle_question(request, [cord19EN], robertaCovidEQA, bertRsp)

## All combined
@app.route('/muheqa/all/en', methods=['GET'])
@app.route('/muheqa/all', methods=['GET'])
def get_all_en():
    return handle_question(request, [dbpediaEN, wikidataEN, cord19EN], robertaCovidEQA, bertRsp)

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error('Page not found. Method: %s uri: %s', request.method, request.path)
    return jsonify({'error':"Page not found..."}), 404

@app.errorhandler(401)
def unauthorized(error):
    app.logger.error('Unauthorized. Method: %s uri: %s', request.method, request.path)
    return jsonify({'error':"Unauthorized."}), 401

@app.errorhandler(405)
def method_not_allowed(error):
    app.logger.error('Method not allowed. Method: %s uri: %s', request.method, request.path)
    return jsonify({'error':"Method not allowed."}), 401
