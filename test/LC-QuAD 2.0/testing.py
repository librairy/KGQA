import pandas as pd
import re
from pprint import pprint

def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield (key, value)
            yield from recursive_items(value)
        else:
            yield (key, value)

"""
a = {
    'a': {"b": {"c": 2, 
              "d": 4}, 
          "e": {"f": 6}
        }

}

for key, value in recursive_items(a):
    if (key == "b"):
        print(key, value)


for k, v in a.items():
    for k1, v1 in v.items():
        print(k1)
"""

df = pd.read_csv("Entities.csv", sep=";")

line = df.iloc[-3,0]
print(line)
line = re.sub('[<>{}]', '', line)
print(line)

line = df.iloc[-5,3]
print(line)
line = re.sub('[\[\]\'\']', '', line)
print(line)
print(type(line))


"""
for i in df['Entities/Answer']:
    print(re.sub('[\[\]\'\']', '', i))
"""

dictList = df.to_dict('records')

for i in dictList:
    print(re.sub('[\[\]\'\']', '', i['Entities/Answer']))

#print(type(df.iloc[-1,3]))