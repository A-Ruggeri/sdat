#import
import mongoHelper
import pandas
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt


class DecisionTree(mongoHelper.MongoHelper):
    def __init__(self):
        super(DecisionTree, self).__init__()

        print("Decision Tree")

        # Default tuning parameters
        self.__precTrain = 30
        self.__maxTreeDepth = 3
        self.__minSplitNum = -1
        self.__maxFeatures = 1

        # Override based on provided json info
        #for k, v in dictionary.items():
            #setattr(self, k, v)


    def setMaxTreeDepth(self, depth):
        """
        Sets the max tree depth ('max_depth').
        Args:
            depth (int): The max tree depth.

        Returns: NONE
        """
        if depth.is_integer() == False:
            print("Decision Tree depth must be an integer.")
            return

        self.__maxTreeDepth = depth
        print(f"\tDecision Tree depth is set to {self.__maxTreeDepth}")


    def setMinSplitNum(self, minSplitNum):
        """
        Sets the min sample amount for a split ('min_samples_split').
        Args:
            minSplitNum (int): Min number of samples to split a node
        Returns: NONE
        """
        if minSplitNum.is_integer() == False:
            print("Decision Tree split number must be an integer.")
            return

        self.__minSplitNum = minSplitNum
        print(f"\tDecision Tree min split number is set to {self.__precTrain}")


    def setMaxFeatures(self, maxFeatures):
        """
        Sets the max feature amount to be used when creating a tree ('max_features').
        Args:
            maxFeatures (int): Max number of features to use for split
        Returns: NONE
        """
        if maxFeatures.is_integer() == False:
            print("Decision Tree max features number must be an integer.")
            return

        self.__maxFeatures = maxFeatures
        print(f"\tDecision Tree max features number is set to {self.__precTrain}")


    def setTrainingDataSet(self, precTrain):
        """
        Set the percentage of data to allocate for training set.
        Args:
            precTrain (int): whole number percentage of data to allocate for training set

        Returns: NONE
        """
        if (precTrain.is_integer() == False) or (precTrain < 1):
            print("NO only whole nuber value: 30% => 30")
            return

        self.__precTrain = precTrain
        print(f"\tSet training data set size to {self.__precTrain}%")


    # ------------------------------------------------------------------
    # decisionTree
    # ------------------------------------------------------------------
    def calculate(self):
        """
        Create a decision tree.
        Returns: tree
        """

        # All the added terms, are the features we want to base the tree off of
        features = list(self.searchDict.keys())

        X = self.dataFrame[features]
        y = self.dataFrame['PDC_NON_ADHR']


        dtree = DecisionTreeClassifier(max_depth = self.__maxTreeDepth,
                                       max_features = self.__maxFeatures)
        dtree = dtree.fit(X, y)

        # nada tada!
        tree.plot_tree(dtree, feature_names=features)

        #hmm
        plt.figure(figsize=(30, 10), facecolor='k')
        a = tree.plot_tree(dtree,
                           feature_names=features,
                           rounded=True,
                           filled=True,
                           fontsize=14)
        plt.show()

        # or
        tree_rules = tree.export_text(dtree,  feature_names=list(features))
        print(tree_rules)

