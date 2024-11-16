#imports
from compute.dataInput.dataInputBase import dataInputBase


class dataCsvFile(dataInputBase):
    def __init__(self, jsonConfig: dict, **kwargs):
        print("CSV File Source")
        super(dataCsvFile, self).__init__(jsonConfig)
        self.classTypeName = "CSV File"

    def addIndependantVar(self, collName, field, binningParam):
        print("Add Independent Variables, not supported")
        return

