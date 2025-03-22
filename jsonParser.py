#imports

import os
import json
import pathlib
from datetime import datetime
from compute.dataInput.dataObjFactory import dataObjFactory
import compute.computeBase

import compute.decisionTree
import compute.neuralNetwork
# import compute.logisticRegression
from compute.helper.loging import printError


def jsonParser(filename):
    fs = open(filename, 'r')
    jsonDict = json.load(fs)


    # Setup dataInput instance and get 'data'
    dof = dataObjFactory()
    dof.createDataSource(jsonDict["dataSource"])
    dof.getDataInputSource()



    # Form Computation Type
    compElement: compute.computeBase.computeBase

    if "decisionTree" in jsonDict.keys():
        compElement = compute.decisionTree.DecisionTree(**jsonDict["decisionTree"])

    elif "neuralNetwork" in jsonDict.keys():
        compElement = compute.neuralNetwork.NeuralNetwork(**jsonDict["neuralNetwork"])
    #
    # elif "logisticRegression" in jsonDict.keys():
    #     compElement = compute.logisticRegression.LogisticRegression(**jsonDict["logisticRegression"])

    else:
        printError("No computation type provided")
        return # kick out as this has failed with nothing to do


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
    compElement.calculate(outputDirectory)

    # Test the model
    compElement.test()

    # Now Done
    return True
