from logging.handlers import RotatingFileHandler
import unittest
import inspect

import application.summary.kg.dbpedia.DBpediaEN as dbpedia_en
import application.summary.kg.wikidata.WikidataEN as wikidata_en
import application.summary.txt.Cord19EN as cord19_en
import application.extraction.BertEQA as bert_en
import application.extraction.RobertaCovidEQA as roberta_covid_en
import application.extraction.RobertaEQA as roberta_en
import application.response.BertAnswererEN as response_en
import application.workflow as wf
import application.datasets.covid19QA.covidqa_dataset as dataset

# Summary
dbpediaEN = dbpedia_en.DBpediaEN()
dbpedia_lm_EN = dbpedia_en.DBpediaEN(rules=False)
wikidataEN = wikidata_en.WikidataEN()
wikidata_lm_EN = wikidata_en.WikidataEN(rules=False)
cord19EN = cord19_en.Cord19EN()

# Extraction
bertEQA = bert_en.BertEQA()
robertaCovidEQA = roberta_covid_en.RobertaCovidEQA()
robertaEQA = roberta_en.RobertaEQA()

# Response
bertRsp = response_en.BertAnswererEN()

class CovidTest(unittest.TestCase):

    def setUp(self):
        print("###############  Test:")
        self.input_data = "application/datasets/covid19QA/data/COVID-QA.json"
        self.dataset    = dataset.CovidQADataset(input_file=self.input_data)
        self.size       = 2019
        self.entities   = False
        self.out_folder = "results/"

    def tearDown(self):
        print("Test done!")

    ############################################################################
    ###     robertaCovidEQA
    ############################################################################

    #@unittest.skip
    def test_covid_000(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        summary     = [cord19EN]
        extraction  = robertaCovidEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=self.out_folder+test_name,limit=self.size,use_entities=self.entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    #@unittest.skip
    def test_covid_001(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        summary     = [dbpediaEN,wikidataEN,cord19EN]
        extraction  = robertaCovidEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=self.out_folder+test_name,limit=self.size,use_entities=self.entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    #@unittest.skip
    def test_covid_002(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        summary     = [dbpedia_lm_EN,wikidata_lm_EN,cord19EN]
        extraction  = robertaCovidEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=self.out_folder+test_name,limit=self.size,use_entities=self.entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    ############################################################################
    ###     bertEQA
    ############################################################################

    #@unittest.skip
    def test_covid_003(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        summary     = [cord19EN]
        extraction  = bertEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=self.out_folder+test_name,limit=self.size,use_entities=self.entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    #@unittest.skip
    def test_covid_004(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        summary     = [dbpediaEN,wikidataEN,cord19EN]
        extraction  = bertEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=self.out_folder+test_name,limit=self.size,use_entities=self.entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    #@unittest.skip
    def test_covid_005(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        summary     = [dbpedia_lm_EN,wikidata_lm_EN,cord19EN]
        extraction  = bertEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=self.out_folder+test_name,limit=self.size,use_entities=self.entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    ############################################################################
    ###     robertaEQA
    ############################################################################

    #@unittest.skip
    def test_covid_006(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        summary     = [cord19EN]
        extraction  = robertaEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=self.out_folder+test_name,limit=self.size,use_entities=self.entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    #@unittest.skip
    def test_covid_007(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        summary     = [dbpediaEN,wikidataEN,cord19EN]
        extraction  = robertaEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=self.out_folder+test_name,limit=self.size,use_entities=self.entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    #@unittest.skip
    def test_covid_008(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        summary     = [dbpedia_lm_EN,wikidata_lm_EN,cord19EN]
        extraction  = robertaEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=self.out_folder+test_name,limit=self.size,use_entities=self.entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)


if __name__ == '__main__':
    import xmlrunner

    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False,
        buffer=False,
        catchbreak=False)
