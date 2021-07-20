# Author: Rafael Ines Guillen
# Project: Explainable QA over KG
# File: manage.py
# Purpose: starts and manage the API REST 


# Loading libraries and dependencies

from flask_script import Manager

from application.app import app
from flask import Flask


# API boot

manager = Manager(app)
app.config['DEBUG'] = False

@manager.command
@manager.option('-h', '--host', dest='host', default='0.0.0.0')
@manager.option('-p', '--port', dest='port', default=5000)
def runprodserver(host='0.0.0.0',port=5000):
    'Run flask server in a production enviroment with host 0.0.0.0 and port 5000 by default.'
    from waitress import serve
    serve(app, host=host, port=port)

if __name__ == '__main__':
    manager.run()
