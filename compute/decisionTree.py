#import
import compute.computeBase
import pandas
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

from compute.dataInput.dataObjFactory import dataObjFactory


class DecisionTree(compute.computeBase.computeBase):
    def __init__(self, **kwargs):
        super(DecisionTree, self).__init__()

        print("Decision Tree")

        # Default tuning parameters
        self.precTrain = 30
        self.maxTreeDepth = 3
        self.minSplitNum = 2
        self.maxFeatures = 1

        # Change from default values based on json
        self.__dict__.update(kwargs)

    def __str__(self):
        """
        Override the string function for this class
        """
        return f"<Decision Tree:\n\tMax Tree Depth: {self.maxTreeDepth}>\n\tMin Split Number: {self.minSplitNum}\n\tMax Feature: {self.maxFeatures}"


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

        self.maxTreeDepth = depth
        print(f"\tDecision Tree depth is set to {self.maxTreeDepth}")


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

        self.minSplitNum = minSplitNum
        print(f"\tDecision Tree min split number is set to {self.precTrain}")


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

        self.maxFeatures = maxFeatures
        print(f"\tDecision Tree max features number is set to {self.precTrain}")


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

        self.precTrain = precTrain
        print(f"\tSet training data set size to {self.precTrain}%")


    # ------------------------------------------------------------------
    # decisionTree
    # ------------------------------------------------------------------
    def calculate(self, outputFolder):
        """
        Create a decision tree.
        Returns: tree
        """

        dof = dataObjFactory()
        if dof.isInitiated() is False:
            print("No data source set up, can not calculate decision tree.")
            return

        dataSource = dof.getDataInputSource()


        # All the added terms, are the features we want to base the tree off of
        features = list(dataSource.searchDict.keys())

        X = dataSource.dataFrame[features]
        y = dataSource.dataFrame['PDC_NON_ADHR']


        # Create the model
        dtree = DecisionTreeClassifier(max_depth = self.maxTreeDepth,
                                       min_samples_split = self.minSplitNum,
                                       max_features = self.maxFeatures)
        dtree = dtree.fit(X, y)

        # Do we need to save the tree model as well?


        # Create graphviz
        tree.plot_tree(dtree, feature_names=features)
        # tree.export_graphviz()


        # Create matlibplot

        # Adjust plotsize based on max_depth
        plot_width = 10 * self.maxTreeDepth
        plot_height = 5 * self.maxTreeDepth
        plt.figure(figsize=(plot_width, plot_height))
        a = tree.plot_tree(dtree,
                           feature_names=features,
                           rounded=True,
                           filled=True,
                           fontsize=14)
        if outputFolder is not None:
            plt.savefig(outputFolder + "/pyplotTree.png",
                        facecolor="w",
                        dpi = 480)
            plt.close()
        else:
            plt.show()


        # Tree text output
        tree_rules = tree.export_text(dtree, feature_names=list(features))
        if outputFolder is not None:
            with open(outputFolder + "/tree_rules.txt", 'w+') as f:
                f.write(tree_rules)
                f.close()
        else:
            print(tree_rules)



        return tree


