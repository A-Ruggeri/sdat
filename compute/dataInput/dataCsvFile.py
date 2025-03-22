# imports
import os.path

import pandas
from compute.helper.loging import printError, printInfo
from compute.dataInput.dataInputBase import dataInputBase


class dataCsvFile(dataInputBase):

    sourceName = "csvFile"


    def __init__(self, jsonConfig: dict, **kwargs):
        self.filePath = ""
        self.__dict__.update(jsonConfig[self.sourceName])

        super(dataCsvFile, self).__init__(jsonConfig)


    def addData(self, dataDict: dict):

        # Change from default values based on json
        self.__dict__.update(dataDict)

        if self.filePath == "":
            printError("CSV File Path Not Provided")
            return

        if not os.path.isfile(self.filePath):
            printError("CSV File Path invalid")
            return

        printInfo(f"Loading data from: {self.filePath}")

        # let's try to read it
        self.dataFrame = pandas.read_csv(self.filePath)







