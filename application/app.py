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



app = Flask(__name__)
app.config.from_object(config)

cors = CORS(app)

dbpediaEN = dbpedia_en.DBpediaEN()
dbpediaES = dbpedia_es.DBpediaES()
wikidataEN = wikidata_en.WikidataEN()
wikidataES = wikidata_es.WikidataES()
cord19EN = cord19_en.Cord19EN()
bertEN = bert_en.BertEN()
robertaCovidEN = roberta_covid_en.RobertaCovidEN()
robertaEN = roberta_en.RobertaEN()
answererEN = answerer_en.AnswererEN()


def decapitalize(str):
    return str[:1].lower() + str[1:]


@app.before_request
def before_request():
    app.logger.info('Request with question: %s for the uri %s .', request.method, request.path)


def handle_question(request,summarizer_list,extractive_qa,response_builder):
    question = request.form['question']
    if 'query' in request.args:
        question = request.args.get('question')
    text = request.args.get('text')
    print("Making question:",question,"..")

    if question is None:
        return jsonify({'error': 'question not received.'}), 200
    
    # Compose Summary
    question = decapitalize(question)
    summary = ""
    for summarizer in summarizer_list:
        partial_summary = summarizer.get_summary(question)
        summary += partial_summary + " "
    
    # Extract Answer   
    answer = extractive_qa.get_answer(question,summary)
    
    # Create Reponse
    value = response_builder.get_response(question, answer['value'])
        
    # Return value
    response = {}
    response['question'] = question
    response['answer'] = value[0]
    response['answer-2'] = value[1]
    response['score'] = answer['score']
    if text.lower() == 'true':
        response['text'] = answer['summary']
    else:
        response['textLen'] = len(answer['summary']) 
    
    print("Response: ", response['answer'])
    
    return jsonify(response), 200


## English DBpedia 
@app.route('/eqakg/dbpedia/en', methods=['GET'])
@app.route('/eqakg/dbpedia', methods=['GET'])
def get_dbpedia_en():
    return handle_question(request, [dbpediaEN], robertaEN, answererEN)

## Spanish DBpedia 
@app.route('/eqakg/dbpedia/es', methods=['GET'])
def get_dbpedia_es():
    return handle_question(request, [dbpediaES], robertaEN, answererEN)

## English Wikidata 
@app.route('/eqakg/wikidata/en', methods=['GET'])
@app.route('/eqakg/wikidata', methods=['GET'])
def get_wikidata_en():
    return handle_question(request, [wikidataEN], robertaEN, answererEN)

## Spanish Wikidata 
@app.route('/eqakg/wikidata/es', methods=['GET'])
def get_wikidata_es():
    return handle_question(request, [wikidataES], robertaEN, answererEN)

## English DBpedia 
@app.route('/eqakg/cord19/en', methods=['GET'])
@app.route('/eqakg/cord19', methods=['GET'])
def get_cord19_en():
    return handle_question(request, [cord19EN], robertaCovidEN, answererEN)

## All combined 
@app.route('/eqakg/all/en', methods=['GET'])
@app.route('/eqakg/all', methods=['GET'])
def get_all_en():
    return handle_question(request, [dbpediaEN, cord19EN], robertaEN, answererEN)

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
