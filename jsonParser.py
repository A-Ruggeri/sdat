#imports

import sys
import os
import json
import decisionTree
from datetime import datetime

def jsonParser(filename):
    fs = open(filename, 'r')
    data = json.load(fs)


    # Get Computation Type
    if "decisionTree" in data.keys():
        dtData = data["decisionTree"]
        dt = decisionTree.DecisionTree(**data["decisionTree"])
        #dt = decisionTree(**data["decisionTree"])

        if "data" in data.keys():
            dataData = data["data"]
            for col in dataData:
                for field in dataData[col]:
                    for featureName, catagoryStr in field.items():  # this is just 1 element, not sure if needed
                        dt.addIndependantVar(col, featureName, catagoryStr)


    # Where do we send all the data?
    outputDirectory = ""    # default to no where
    if "output" in data.keys():
        outData = data["output"]

        # Set the output directory to CWD unless overrode
        outputDirectory = os.getcwd()

        # Check if directory location set
        if "directory" in outData:
            outputDirectory = outData["directory"]

        # should a timestamp be appended to the directory?
        if "timestamp" in outData:
            now = datetime.now()
            outputDirectory += now.strftime("_%Y-%m-%d_%H-%M")

        # save Json too?
        if "saveJson" in outData:
            print("DO NOTHING FOR NOW")
            # with open(outputDirectory + "/config.json", 'w+') as f:
                # f.write(json.dumps(data, indent=4))

    # Calculate and save
    dt.calculate(outputDirectory)

    return True
