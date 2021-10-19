# Author: Rafael Ines Guillen
# Project: Explainable QA over KG
# File: app.py
# Purpose: questions treatment


# Loading libraries

from flask import Flask, request, abort, jsonify, send_from_directory#, session,
from logging.handlers import RotatingFileHandler
from application import config
from flask_cors import CORS

import datetime
import logging
import json
import os


# Initialize variables

app = Flask(__name__)
app.config.from_object(config)

cors = CORS(app)

@app.before_request
def before_request():
    app.logger.info('Request with question: %s for the uri %s .', request.method, request.path)


# Loading dependencies

import application.DBpedia as DBpediaEN
import application.DBpediaES as DBpediaES
import application.WikidataEN as WikidataEN


# Question part

## Check question

@app.route('/eqakg/question', methods=['GET'])
def get_question():
    question = request.form['question']
    text = request.args.get('text')

    if question is None:
        return jsonify({'error': 'question not recived.'}), 200
    
    if text != 'true':
        return jsonify({'answer': question}), 200
    
    return jsonify({'answer': question, 'text': 'true'}), 200


## DBpedia in english

@app.route('/eqakg/dbpedia/en', methods=['GET'])
@app.route('/eqakg/dbpedia', methods=['GET'])
def get_debpediaEN():
    question = request.form['question']
    text = request.args.get('text')

    if question is None:
        return jsonify({'error': 'question not recived.'}), 200
    
    aux = DBpediaEN.DBpedia(question)
    if text != 'true':
        if aux[1] is not None:
            return jsonify({'question': question, 'answer': aux[0], 'textLen': len(aux[1])}), 200
        else:
            return jsonify({'question': question, 'answer': aux[0], 'textLen': 'None'}), 200

    
    return jsonify({'question': question, 'answer': aux[0], 'text': aux[1]}), 200


## DBpedia in spanish

@app.route('/eqakg/dbpedia/es', methods=['GET'])
def get_debpediaES():
    question = request.form['question']
    text = request.args.get('text')

    if question is None:
        return jsonify({'error': 'question not recived.'}), 200
    
    aux = DBpediaES.DBpedia(question)
    if text != 'true':
        return jsonify({'question': question, 'answer': aux[0]}), 200
    
    return jsonify({'question': question, 'answer': aux[0], 'text': aux[1]}), 200


## Wokodata in english

@app.route('/eqakg/wikidata/en', methods=['GET'])
@app.route('/eqakg/wikidata', methods=['GET'])
def get_wikidataEN():
    question = request.form['question']
    text = request.args.get('text')

    if question is None:
        return jsonify({'error': 'question not recived.'}), 200
    
    aux = WikidataEN.WikidataEN(question)
    if text != 'true':
        return jsonify({'question': question, 'answer': aux[0]}), 200
    
    return jsonify({'question': question, 'answer': aux[0], 'text': aux[1]}), 200


# Error handler

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
