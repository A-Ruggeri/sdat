# imports
import os.path

import pandas
from compute.loging import printError, printInfo
from compute.dataInput.dataInputBase import dataInputBase


class dataCsvFile(dataInputBase):
    def __init__(self, jsonConfig: dict, **kwargs):
        print("CSV File Source")
        super(dataCsvFile, self).__init__(jsonConfig)

        filePath = ""

        # Change from default values based on json
        self.__dict__.update(kwargs)

        if filePath == "":
            printError("CSV File Path Not Provided")
            return

        if not os.path.isfile(filePath):
            printError("CSV File Path invalid")
            return

        # let's try to read it
        self.dataframe = pandas.read_csv(filePath)





