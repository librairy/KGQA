from logging.handlers import RotatingFileHandler
import unittest
import inspect
import json

import application.evaluation as eval

evaluation  = eval.Evaluation()

class EvalTest(unittest.TestCase):

    def setUp(self):
        self.input_folder = "results/"
        self.size         = "10"
        self.query_types  = ["how","where","what","who","when","which","is","in"]

    def tearDown(self):
        print("Evaluation done!")

    def evaluate(self,input_file):
        print("###############  Evaluation of",input_file)
        output_file = input_file.split(".json")[0]+"_evaluation.json"
        count = 0
        with open(output_file, 'w') as json_writer:
            result      = evaluation.run(input_file)
            json_writer.write(json.dumps(result, ensure_ascii=False)+"\n")
            count += 1

            for query_type in self.query_types:
                filter = query_type
                filter_result  = evaluation.run(input_file,filter)
                json_writer.write(json.dumps(filter_result, ensure_ascii=False)+"\n")
                count += 1
        self.assertEqual(count, len(self.query_types)+1)

    ############################################################################
    ###     Wikidata
    ############################################################################

    def test_fq_000(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        self.evaluate(self.input_folder+test_name)


    def test_fq_001(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        self.evaluate(self.input_folder+test_name)

    def test_fq_002(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        self.evaluate(self.input_folder+test_name)

    def test_fq_003(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        self.evaluate(self.input_folder+test_name)

    def test_fq_004(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        self.evaluate(self.input_folder+test_name)

    def test_fq_005(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        self.evaluate(self.input_folder+test_name)

    def test_fq_006(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        self.evaluate(self.input_folder+test_name)

    def test_fq_007(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        self.evaluate(self.input_folder+test_name)


    ############################################################################
    ###     DBpedia
    ############################################################################

    def test_fq_008(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        self.evaluate(self.input_folder+test_name)

    def test_fq_009(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        self.evaluate(self.input_folder+test_name)

    def test_fq_010(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        self.evaluate(self.input_folder+test_name)

    def test_fq_011(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        self.evaluate(self.input_folder+test_name)

    ############################################################################
    ###     Wikidata+DBpedia
    ############################################################################

    def test_fq_012(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        self.evaluate(self.input_folder+test_name)

    def test_fq_013(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        self.evaluate(self.input_folder+test_name)

    def test_fq_014(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        self.evaluate(self.input_folder+test_name)

    def test_fq_015(self):
        test_name   = inspect.stack()[0][3]+"_"+str(self.size)+".json"
        self.evaluate(self.input_folder+test_name)

if __name__ == '__main__':
    import xmlrunner

    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False,
        buffer=False,
        catchbreak=False)
