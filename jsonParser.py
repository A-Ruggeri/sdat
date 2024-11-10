#imports

import sys
import json

def jsonParser(filename):
    fs = open(filename, 'r')
    data = json.load(fs)

    if "decisionTree" in data.keys():
        dtData = data["decisionTree"]
        #decisionTree(**data["decisionTree"])
    return False