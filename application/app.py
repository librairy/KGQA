from flask import Flask, request, abort, jsonify, send_from_directory#, session,
from logging.handlers import RotatingFileHandler
from application import config
from flask_cors import CORS

import application.summary.DBpediaEN as dbpedia_en
import application.summary.DBpediaES as dbpedia_es
import application.summary.WikidataEN as wikidata_en
import application.summary.WikidataES as wikidata_es
import application.extraction.BertEN as bert_en


app = Flask(__name__)
app.config.from_object(config)

cors = CORS(app)

dbpediaEN = dbpedia_en.DBpediaEN()
dbpediaES = dbpedia_es.DBpediaES()
wikidataEN = wikidata_en.WikidataEN()
wikidataES = wikidata_es.WikidataES()
bertEN = bert_en.BertEN()


def decapitalize(str):
    return str[:1].lower() + str[1:]


@app.before_request
def before_request():
    app.logger.info('Request with question: %s for the uri %s .', request.method, request.path)


def handle_question(request,kg_summarizer):
    question = request.form['question']
    text = request.args.get('text')

    if question is None:
        return jsonify({'error': 'question not received.'}), 200
    
    question = decapitalize(question)
    summary = kg_summarizer.get_summary(question)
    answer = bertEN.get_answer(question,summary)
    response = {}
    response['question'] = question
    response['answer'] = answer['value']
    response['score'] = answer['score']
    if text.lower() == 'true':
        response['text'] = summary
    else:
        response['textLen'] = len(summary) 
    
    return jsonify(response), 200


## English DBpedia 
@app.route('/eqakg/dbpedia/en', methods=['GET'])
@app.route('/eqakg/dbpedia', methods=['GET'])
def get_dbpedia_en():
    return handle_question(request, dbpediaEN)

## Spanish DBpedia 
@app.route('/eqakg/dbpedia/es', methods=['GET'])
def get_dbpedia_es():
    return handle_question(request, dbpediaES)

## English Wikidata 
@app.route('/eqakg/wikidata/en', methods=['GET'])
@app.route('/eqakg/wikidata', methods=['GET'])
def get_wikidata_en():
    return handle_question(request, wikidataEN)

## Spanish Wikidata 
@app.route('/eqakg/wikidata/es', methods=['GET'])
def get_wikidata_es():
    return handle_question(request, wikidataES)


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
