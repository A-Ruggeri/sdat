# imports
import pymongo
import pandas
import numpy
import dataNameHelper

class MongoBase:
    """
    singleton class to handle connection to MongoDB server.
    """
    def __new__(cls, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MongoBase, cls).__new__(cls)
        return cls.instance


    def __init__(self,  **kwargs):
        print("monobase")
        # Try/catch connection to database
        # try:
        #     self.__client = pymongo.MongoClient('localhost', 27017, serverSelectionTimeoutMS=5000)
        #     self.__client.server_info()
        #
        # except pymongo.errors.ServerSelectionTimeoutError as err:
        #     print("Failed to connect to Mongod service")
        #     return
        #
        # self.__db = self.__client['seer']
        # self.collcPdcMpr = self.__db['PDESAF_pdc_mpr_results']




class MongoHelper(MongoBase):
    """
    class to handle reading data from MongoDB.
    """
    def __init__(self, **kwargs):
        super(MongoHelper, self).__init__()
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
        self.searchDict = dict()

        print(f"\tPDC PIDS: {len(self.dataFrame.index)}")



    # ------------------------------------------------------------------
    # addIndependantVar
    # ------------------------------------------------------------------
    def addIndependantVar(self, collName, field, binningParam):
        """ Add an additional column of data.
        Args:
            collName (str): Collection Name
            field (str): field name
            binningParam (str): True/positive conditions string
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



    # ------------------------------------------------------------------
    # addCategoricalIndependantVar
    #   This should/could be merged with the addIndependantVar
    # ------------------------------------------------------------------
    def addCategoricalIndependantVar(self, collName, field, posSearch):
        print("----------------------------------------------------")
        print(f"Categorically Adding {field} in {collName} with {posSearch}")

        dfFieldName = field #+ '_' + posSearch.replace('\n', '').replace(',', '_')
        self.searchDict[dfFieldName] = dfFieldName
        posSearch = posSearch.replace('\n', '').split(',')


        collcFields = self.__db[collName]
        self.dataFrame[dfFieldName] = numpy.nan

        fieldRes = collcFields.find({'$and': [{'PATIENT_ID': {'$in': list(self.dataFrame.index)}}, {field: {'$exists': True}}]}).sort("PATIENT_ID", pymongo.DESCENDING)

        for record in fieldRes:
            pid = record["PATIENT_ID"]
            value = str(record[field])

            # check for duplicates while we do this
            if str(record[field]) in posSearch:
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