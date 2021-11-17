import pandas as pd
import json
from pprint import pprint

def JSONLineToDict(JSONRoute,JSON):
    '''
    df = pd.read_json(JSONRoute, lines=True)
    df.to_json(JSON)
    '''  

    with open(JSONRoute) as f:
        jsonList = list(f)
    
    return json.dumps([json.loads(jsonLine) for jsonLine in jsonList])

    '''
    for json_str in json_list:
        result = json.loads(json_str)
        print(f"result: {result}")
    '''
   
pprint(JSONLineToDict("Vanilla_Dataset_Test.json","test.json"))

