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
import application.datasets.forwardquestions.fqdataset as fqd

dbpediaEN = dbpedia_en.DBpediaEN()
dbpedia_lm_EN = dbpedia_en.DBpediaEN(rules=False)
wikidataEN = wikidata_en.WikidataEN()
wikidata_lm_EN = wikidata_en.WikidataEN(rules=False)
cord19EN = cord19_en.Cord19EN()
bertEQA = bert_en.BertEQA()
robertaCovidEQA = roberta_covid_en.RobertaCovidEQA()
robertaEQA = roberta_en.RobertaEQA()
bertRsp = response_en.BertAnswererEN()

class FQTest(unittest.TestCase):

    def setUp(self):
        print("###############  Test:")
        self.input_data = "application/datasets/forwardquestions/data/all_questions.json"
        self.dataset    = fqd.ForwardQuestionsDataset(input_file=self.input_data)
        self.size       = 100

    def tearDown(self):
        print("Test done!")

    ############################################################################
    ###     Wikidata
    ############################################################################

    def test_fq_000(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        entities    = False
        summary     = [wikidataEN]
        extraction  = bertEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=test_name,limit=self.size,use_entities=entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    def test_fq_001(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        entities    = False
        summary     = [wikidata_lm_EN]
        extraction  = bertEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=test_name,limit=self.size,use_entities=entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    def test_fq_002(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        entities    = True
        summary     = [wikidataEN]
        extraction  = bertEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=test_name,limit=self.size,use_entities=entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    def test_fq_003(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        entities    = True
        summary     = [wikidata_lm_EN]
        extraction  = bertEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=test_name,limit=self.size,use_entities=entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    def test_fq_004(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        entities    = False
        summary     = [wikidataEN]
        extraction  = robertaEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=test_name,limit=self.size,use_entities=entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    def test_fq_005(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        entities    = False
        summary     = [wikidata_lm_EN]
        extraction  = robertaEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=test_name,limit=self.size,use_entities=entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    def test_fq_006(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        entities    = True
        summary     = [wikidataEN]
        extraction  = robertaEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=test_name,limit=self.size,use_entities=entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    def test_fq_007(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        entities    = True
        summary     = [wikidata_lm_EN]
        extraction  = robertaEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=test_name,limit=self.size,use_entities=entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)


    ############################################################################
    ###     DBpedia
    ############################################################################

    def test_fq_008(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        entities    = False
        summary     = [dbpediaEN]
        extraction  = bertEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=test_name,limit=self.size,use_entities=entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    def test_fq_009(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        entities    = False
        summary     = [dbpedia_lm_EN]
        extraction  = bertEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=test_name,limit=self.size,use_entities=entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    def test_fq_010(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        entities    = False
        summary     = [dbpediaEN]
        extraction  = robertaEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=test_name,limit=self.size,use_entities=entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    def test_fq_011(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        entities    = False
        summary     = [dbpedia_lm_EN]
        extraction  = robertaEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=test_name,limit=self.size,use_entities=entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    ############################################################################
    ###     Wikidata+DBpedia
    ############################################################################

    def test_fq_012(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        entities    = False
        summary     = [wikidataEN,dbpediaEN]
        extraction  = bertEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=test_name,limit=self.size,use_entities=entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    def test_fq_013(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        entities    = False
        summary     = [wikidata_lm_EN,dbpedia_lm_EN]
        extraction  = bertEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=test_name,limit=self.size,use_entities=entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    def test_fq_014(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        entities    = False
        summary     = [wikidataEN,dbpediaEN]
        extraction  = robertaEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=test_name,limit=self.size,use_entities=entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

    def test_fq_015(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        entities    = False
        summary     = [wikidata_lm_EN,dbpedia_lm_EN]
        extraction  = robertaEQA
        response    = bertRsp
        workflow    = wf.Workflow(summary,extraction,response)
        count       = self.dataset.test(workflow,file_name=test_name,limit=self.size,use_entities=entities,get_evidence=True,pool_size=1)
        self.assertEqual(count, self.size)

if __name__ == '__main__':
    import xmlrunner

    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False,
        buffer=False,
        catchbreak=False)
