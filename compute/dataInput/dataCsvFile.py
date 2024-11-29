# imports
import os.path

import pandas
from compute.loging import printError, printInfo
from compute.dataInput.dataInputBase import dataInputBase


class dataCsvFile(dataInputBase):

    sourceName = "csvFile"


    def __init__(self, jsonConfig: dict, **kwargs):
        super(dataCsvFile, self).__init__(jsonConfig)


    def addData(self, dataDict: dict):
        filePath = ""

        # Change from default values based on json
        self.__dict__.update(dataDict)

        if filePath == "":
            printError("CSV File Path Not Provided")
            return

        if not os.path.isfile(filePath):
            printError("CSV File Path invalid")
            return

        # let's try to read it
        self.dataframe = pandas.read_csv(filePath)






