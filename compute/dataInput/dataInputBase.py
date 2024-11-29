# imports
import pandas
import sklearn
from compute.loging import printInfo, printError


class dataInputBase:
    # """
    # singleton class to handle connection to MongoDB server.
    # """
    # def __new__(cls, **kwargs):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(dataInputBase, cls).__new__(cls)
    #     return cls.instance

    sourceName = "base"

    def __init__(self,  jsonConfig: dict, **kwargs):
        self.searchDict = dict()                # dict to field names : field named + query settings
        self.dataFrame: pandas.DataFrame        # primary dataframe, holds all data read from database
        self.X_train: pandas.DataFrame
        self.X_test: pandas.DataFrame
        self.y_train
        self.y_test

        self.trainingFrame: pandas.DataFrame    # Training dataframe
        self.testingFrame: pandas.DataFrame     # Testing dataframe

        # Setup data source
        self.setupSource(jsonConfig[self.sourceName])

        # Read data
        if "data" in jsonConfig:
            self.addData(jsonConfig["data"])
        else:
            printError("Missing 'data' key")

        # Setup testing/training data
        if "training" in jsonConfig:
            self.splitData(jsonConfig["training"])




    def addIndependantVar(self, collName, field, binningParam):
        print("addIndependantVar")

    def addCategoricalIndependantVar(self, collName, field, allowedVals):
        print("addCategoricalIndependantVar")

    def classType(self):
        print(f'{self.__class__.__name__} class type')

    def setupSource(self, sourceDict: dict):
        printInfo(f'Setup Source: {self.sourceName}')

    def addData(self, dataDict: dict):
        printInfo("Add Data")

    def splitData(self, splitDict: dict):
        """
        splits the data into training and testing sets
        """
        printInfo("Split Data")
        testSizePerc = None
        randomState = None
        shuffle = True


        if "testSizePercentage" in splitDict:
            testSizePerc = splitDict["testSizePercentage"]

        if "randomSeed" in splitDict:
            randomState = splitDict["randomSeed"]

        if ("shuffle" in splitDict) and (splitDict["shuffle"] == 0):
            shuffle = False


        features = list(self.searchDict.keys())

        self.X_train, self.X_test, self.y_train, self.y_test = sklearn.model_selection.train_test_split(
                                                                              self.dataFrame[features],
                                                                                     self.dataFrame['PDC_NON_ADHR'],
                                                                                     train_size=testSizePerc,
                                                                                     random_state=randomState,
                                                                                     shuffle=shuffle)

        print("done splitting data")