# Imports
import compute.dataInput.dataInputBase
import compute.dataInput.dataMongoDb
import compute.dataInput.dataCsvFile

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton

@singleton
class dataObjFactory:
    __dataInputSource: compute.dataInput.dataInputBase.dataInputBase
    __inited = False

    def __init__(self, **kwargs):
        if self.__inited is True:
            print("Data Object Factory Already Initialized")
        else:
            print("Data Object Factory Initializing")


    def createDataSource(self, jsonDataDict: dict):
        print("Creating Data Source")
        if "mongoDb" in jsonDataDict:
            self.__dataInputSource = compute.dataInput.dataMongoDb.dataMongoDb(jsonDataDict)

        elif "csvFile" in jsonDataDict:
            self.__dataInputSource = compute.dataInput.dataCsvFile.dataCsvFile(jsonDataDict["csvFile"])

        else:
            print("No data source element found in JSON")
            self.__inited = False

        self.__inited = True

    def isInitiated(self):
        return self.__inited

    def getDataInputSource(self):
        if self.__inited is True:
            return self.__dataInputSource
        else:
            return None

