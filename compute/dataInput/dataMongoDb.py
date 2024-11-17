# imports
import pymongo
import pandas
import numpy
import dataNameHelper
import compute.dataInput.dataInputBase



class dataMongoDb(compute.dataInput.dataInputBase.dataInputBase):
    """
    class to handle reading data from MongoDB.
    """
    def __init__(self, jsonConfig: dict, **kwargs):
        super(dataMongoDb, self).__init__(jsonConfig)
        #super().__init__()

        try:
            self.__client = pymongo.MongoClient('localhost', 27017, serverSelectionTimeoutMS=5000)
            self.__client.server_info()

        except pymongo.errors.ServerSelectionTimeoutError as err:
            print("Failed to connect to Mongod service")
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

        self.__dnh = dataNameHelper.dataNameHelper()

        print(f"\tPDC PIDS: {len(self.dataFrame.index)}")

        # populate the database based if provided through the JSON info
        if "test" in kwargs.keys():
            print("found in kwargs")




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

        # Remove duplicates from list of common pids to avoid them getting added then later removed
        # for dupPid in self.__duplicatePids:
        #     self.__dataFrame.drop(dupPid)
        #     self.__commonPids.remove(dupPid)    # is this needed any more?

        # if there is missing data (aka NaN) for a pid drop it
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



    def addFieldCollectionGroup(self, collectionName, fieldGroup):
        """
        Add group of fields within a collection.
        Args:
            collectionName (str): Name of the collection
            fieldGroup (): a tuple list of fields and their binning parameters
                [(fieldA, "a,b,c"), (fieldB, "x,y,z"), ect]

        Returns: NONE
        """