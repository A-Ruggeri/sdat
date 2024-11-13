#imports

import sys
import os
import json
import decisionTree
import pathlib
from datetime import datetime


def jsonParser(filename):
    fs = open(filename, 'r')
    jsonDict = json.load(fs)


    # Get Computation Type
    if "decisionTree" in jsonDict.keys():
        dt = decisionTree.DecisionTree(**jsonDict["decisionTree"])

        if "data" in jsonDict.keys():
            dataData = jsonDict["data"]
            for col in dataData:
                for field in dataData[col]:
                    for featureName, catagoryStr in field.items():  # this is just 1 element, not sure if needed
                        dt.addIndependantVar(col, featureName, catagoryStr)


    # Where do we send all the data?
    outputDirectory = ""    # default to nowhere
    if "output" in jsonDict.keys():
        outData = jsonDict["output"]

        # Set the output directory to CWD unless overrode
        outputDirectory = os.getcwd()

        # Check if directory location set
        if "directory" in outData:
            outputDirectory = outData["directory"]

        # should a timestamp be appended to the directory?
        if "timestamp" in outData:
            now = datetime.now()
            outputDirectory += now.strftime("_%Y-%m-%d_%H-%M")

        # Create output directory, in the case it's not there
        pathlib.Path(outputDirectory).mkdir(parents=True, exist_ok=True)

        # save Json too?
        if "saveJson" in outData:
            with open(outputDirectory + "/config.json", 'w+') as f:
                f.write(json.dumps(jsonDict, indent=4))


    # Calculate and save
    dt.calculate(outputDirectory)

    return True
