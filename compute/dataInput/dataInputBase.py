# imports
import pandas

class dataInputBase:
    # """
    # singleton class to handle connection to MongoDB server.
    # """
    # def __new__(cls, **kwargs):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(dataInputBase, cls).__new__(cls)
    #     return cls.instance


    def __init__(self,  jsonConfig: dict, **kwargs):
        self.searchDict = dict()    # dict to field names : field named + query settings
        self.dataFrame: pandas.DataFrame    # primary dataframe


    def addIndependantVar(self, collName, field, binningParam):
        print("addIndependantVar")

    def addCategoricalIndependantVar(self, collName, field, allowedVals):
        print("addCategoricalIndependantVar")

    def classType(self):
        print(f'{self.__class__.__name__} class type')