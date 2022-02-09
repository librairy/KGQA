from logging.handlers import RotatingFileHandler
import unittest
import inspect

#import application.summary.kg.dbpedia.DBpediaEN as dbpedia_en
import application.summary.kg.wikidata.WikidataEN as wikidata_en
#import application.summary.txt.Cord19EN as cord19_en
import application.extraction.BertEQA as bert_en
#import application.extraction.RobertaCovidEQA as roberta_covid_en
#import application.extraction.RobertaEQA as roberta_en
import application.response.BertAnswererEN as response_en
import application.workflow as wf

#Summary
#dbpediaEN = dbpedia_en.DBpediaEN()
#dbpedia_lm_EN = dbpedia_en.DBpediaEN(rules=False)
wikidataEN = wikidata_en.WikidataEN()
wikidata_lm_EN = wikidata_en.WikidataEN(rules=False)
#cord19EN = cord19_en.Cord19EN()

# Extraction
bertEQA = bert_en.BertEQA()
#robertaCovidEQA = roberta_covid_en.RobertaCovidEQA()
#robertaEQA = roberta_en.RobertaEQA()

# Response
bertRsp = response_en.BertAnswererEN()

# Question
#input_data  = {'question':"What kind of music is rob townsend?", 'entities':"Q3434241;rob townsend"}
input_data  = {'question':"What kind of music is rob townsend?"}

# Workflow
summary     = [wikidata_lm_EN]
extraction  = bertEQA
response    = bertRsp
workflow    = wf.Workflow(summary,extraction,response)
response    = workflow.process(input_data)

# Response
print(response)
