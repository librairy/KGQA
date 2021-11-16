import pandas as pd
import json
from pprint import pprint

def processJSON(JSONRoute,JSON):
    '''
    df = pd.read_json(JSONRoute, lines=True)
    df.to_json(JSON)
    '''  

    with open(JSONRoute) as f:
        json_list = list(f)
    
    output_list = json.dumps([json.loads(JSON_STRING) for JSON_STRING in json_list])
    pprint(output_list)
    return output_list

    '''
    for json_str in json_list:
        result = json.loads(json_str)
        print(f"result: {result}")
    '''

    
processJSON("Vanilla_Dataset_Test.json","test.json")

