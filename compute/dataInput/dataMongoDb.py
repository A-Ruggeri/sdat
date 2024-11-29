# imports
import pymongo
import pandas
import numpy
import compute.dataInput.dataInputBase
from compute.loging import printError


class dataMongoDb(compute.dataInput.dataInputBase.dataInputBase):
    """
    class to handle reading data from MongoDB.
    """

    sourceName = "mongoDb"

    def __init__(self, jsonConfig: dict, **kwargs):
        super(dataMongoDb, self).__init__(jsonConfig)



    def setupSource(self, sourceDict: dict):
        # default connection values, assume running locally
        mongodbIp = "localhost"
        mongodbPort = 27017

        # Grab values from json, if present
        if "ip" in sourceDict:
            mongodbIp = sourceDict["ip"]

        if "port" in sourceDict:
            mongodbPort = sourceDict["port"]

        # Connect to Mongo Server
        try:
            self.__client = pymongo.MongoClient(mongodbIp, port=mongodbPort, serverSelectionTimeoutMS=5000)
            self.__client.server_info()

        except pymongo.errors.ServerSelectionTimeoutError as err:
            printError("Failed to connect to Mongod service")
            return

        self.__db = self.__client['seer']
        self.collcPdcMpr = self.__db['PDESAF_pdc_mpr_results']

        print("\tGet PIDS for PDC")
        pdcValues = dict()
        pdcRes = self.collcPdcMpr.find({'INCLUDED': True}).sort("PATIENT_ID", pymongo.DESCENDING)

        for record in pdcRes:
            pid = record['PATIENT_ID']
            # We are looking if a patient IS non-adherent.
            if record['PDC_ADHERENT'] is False:
                pdcValues[pid] = 1
            else:
                pdcValues[pid] = 0

        self.dataFrame = pandas.DataFrame(
            {'PIDS': list(pdcValues.keys()), 'PDC_NON_ADHR': list(list(pdcValues.values()))})
        self.dataFrame.set_index('PIDS', verify_integrity=True, drop=True, inplace=True)

        print(f"\tPDC PIDS: {len(self.dataFrame.index)}")



    def addData(self, dataDict: dict):
        print("Add Data")

        for col in dataDict:
            for field in dataDict[col]:
                for featureName, catagoryStr in field.items():  # this is just 1 element, not sure if needed
                    self.addIndependantVar(col, featureName, catagoryStr)



    def addIndependantVar(self, collName, field, binningParam):
        """ Add an additional column of data. override from base class
        Args:
            collName (str): Collection Name
            field (str): field name
            binningParam (str): True/positive conditions string (if field's value matches param, will set data value as true)
        Returns: none
        """
        print("----------------------------------------------------")
        print(f"Adding {field} in {collName} with {binningParam}")

        dfFieldName = field + '_' + binningParam.replace('\n', '').replace(',', '_')
        self.searchDict[dfFieldName] = field
        binningParam = binningParam.replace('\n', '').split(',')

        collcFields = self.__db[collName]
        self.dataFrame[dfFieldName] = numpy.nan

        fieldRes = collcFields.find(
            {'$and': [{'PATIENT_ID': {'$in': list(self.dataFrame.index)}}, {field: {'$exists': True}}]}).sort(
            "PATIENT_ID", pymongo.DESCENDING)
        for record in fieldRes:
            pid = record["PATIENT_ID"]

            if str(record[field]) in binningParam:
                self.dataFrame._set_value(pid, dfFieldName, 1)
            else:
                self.dataFrame._set_value(pid, dfFieldName, 0)

        print(f'\tDone:')



    def addCategoricalIndependantVar(self, collName, field, allowedVals):
        """ Add an additional column of data. override from base class
        Args:
            collName (str): Collection Name
            field (str): field name
            allowedVals (str): Allowed cat values, helps filter erronous/unwanted values
        Returns: none
        """
        print("----------------------------------------------------")
        print(f"Categorically Adding {field} in {collName} with {allowedVals}")

        dfFieldName = field #+ '_' + posSearch.replace('\n', '').replace(',', '_')
        self.searchDict[dfFieldName] = dfFieldName
        allowedVals = allowedVals.replace('\n', '').split(',')


        collcFields = self.__db[collName]
        self.dataFrame[dfFieldName] = numpy.nan

        fieldRes = collcFields.find({'$and': [{'PATIENT_ID': {'$in': list(self.dataFrame.index)}}, {field: {'$exists': True}}]}).sort("PATIENT_ID", pymongo.DESCENDING)

        for record in fieldRes:
            pid = record["PATIENT_ID"]
            value = str(record[field])

            # check for duplicates while we do this
            if str(record[field]) in allowedVals:
                self.dataFrame._set_value(pid, dfFieldName, value)
            # else:
            #     self.__dataFrame._set_value(pid, dfFieldName, "OTHER")


        self.dataFrame[dfFieldName] = self.dataFrame[dfFieldName].astype('category')

        # if there is missing data (aka NaN) for a pid drop it
        print(f'\tDone:')
