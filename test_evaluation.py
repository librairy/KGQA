from logging.handlers import RotatingFileHandler
import unittest
import inspect
import json
import application.evaluation as eval
import os

evaluation  = eval.Evaluation()

class EvalTest(unittest.TestCase):

    def setUp(self):
        self.input_folder = "results/"
        self.size         = "10"
        self.query_types  = ["how","where","what","who","when","which","is","in"]

    def tearDown(self):
        print("Evaluation done!")

    def evaluate(self,input_file):
        print("###############  Evaluation of",input_file,"...")
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

    def test_all(self):
        files = []
        for filename in os.scandir(self.input_folder):
            if filename.is_file():
                files.append(filename.path)
        for file in files:
            if (file.endswith('_evaluation.json')):
                continue
            else:
                eval_file = file.split(".json")[0]+"_evaluation.json"
                if (eval_file in files):
                    continue
                else:
                    self.evaluate(file)

if __name__ == '__main__':
    import xmlrunner

    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False,
        buffer=False,
        catchbreak=False)
