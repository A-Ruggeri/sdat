# imports
import pandas
import sklearn
from compute.helper.loging import printInfo, printError


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
        self.features = []                # dict to field names : field named + query settings
        self.dataFrame: pandas.DataFrame        # primary dataframe, holds all data read from database
        self.x_train: pandas.DataFrame
        self.x_test: pandas.DataFrame
        self.y_train = None
        self.y_test = None

        self.trainingFrame: pandas.DataFrame    # Training dataframe
        self.testingFrame: pandas.DataFrame     # Testing dataframe
        self.targetName = "target"

        if "targetName" in jsonConfig:
            self.targetName = jsonConfig["targetName"]

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
            testSizePerc = testSizePerc/100 # Need it as a 0<>1 based float for % split

        if "randomSeed" in splitDict:
            randomState = splitDict["randomSeed"]

        if ("shuffle" in splitDict) and (splitDict["shuffle"] == 0):
            shuffle = False


        self.x_train, self.x_test, self.y_train, self.y_test = sklearn.model_selection.train_test_split(
                                                                              self.dataFrame[self.features],
                                                                                     self.dataFrame[self.targetName],
                                                                                     train_size=testSizePerc,
                                                                                     random_state=randomState,
                                                                                     shuffle=shuffle)

        print(f"Training Size: {len(self.y_train)}")
        print(f"Testing Size: {len(self.y_test)}")
        print("done splitting data")


    def clearIndependentVars(self):
        printInfo("Clearing Independent Variables")

        for colName in self.__dataFrame.columns[1:]:
            print(f'\tSo Long: {colName}')
            self.__dataFrame.drop(colName, axis=1, inplace=True)
        print("cleared")





