#import
import compute.computeBase
import pandas
import sklearn
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt

from compute.loging import printInfo, printStd


class DecisionTree(compute.computeBase.computeBase):
    def __init__(self, **kwargs):
        super(DecisionTree, self).__init__()

        printInfo("Decision Tree")

        # Default tuning parameters
        self.maxTreeDepth = 3
        self.minSplitNum = 2
        self.maxFeatures = 1
        self.randomSeed = None
        self.gridSearch = False

        # Change from default values based on json
        self.__dict__.update(kwargs)

        self.__dtree: sklearn.tree.DecisionTreeClassifier



    def __str__(self):
        """
        Override the string function for this class
        """
        return f"<Decision Tree:\n\tMax Tree Depth: {self.maxTreeDepth}>\n\tMin Split Number: {self.minSplitNum}\n\tMax Feature: {self.maxFeatures}"



    def calculate(self, outputFolder):
        """
        Create a decision tree.
        Returns: tree
        """

        # All the added terms, are the features we want to base the tree off of
        features = list(self.dataSource.searchDict.keys())

        xTrain = self.dataSource.x_train
        yTrain = self.dataSource.y_train


        self.__dtree = DecisionTreeClassifier()

        # Grid Search YES!
        if(self.gridSearch != False):
            printInfo("Grid Search: Enabled")
            param_grid = {
                'criterion': ['gini', 'entropy'],
                'max_depth': self.maxTreeDepth,
                'min_samples_split': self.minSplitNum,
                'max_features': self.maxFeatures,
            }

            gridSearch = GridSearchCV(self.__dtree, param_grid, cv=5)
            gridSearch.fit(xTrain, yTrain)

            printStd(f'Best parameters: {gridSearch.best_params_}')
            self.__dtree = gridSearch.best_estimator_
            self.maxTreeDepth = gridSearch.best_params_["max_depth"]    # Needed for figure size computation

        # No grid search
        else:
            printInfo("Grid Search: Disabled")
            # Create the model
            self.__dtree = DecisionTreeClassifier(max_depth = self.maxTreeDepth,
                                           min_samples_split = self.minSplitNum,
                                           max_features = self.maxFeatures,
                                           random_state = self.randomSeed)

            self.__dtree = self.__dtree.fit(xTrain, yTrain)



        # Create graphviz
        tree.plot_tree(self.__dtree, feature_names=features)
        # tree.export_graphviz()


        # Adjust plotsize based on max_depth
        plot_width = 10 * self.maxTreeDepth
        plot_height = 5 * self.maxTreeDepth
        plt.figure(figsize=(plot_width, plot_height))
        a = tree.plot_tree(self.__dtree,
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
        tree_rules = tree.export_text(self.__dtree, feature_names=list(features))
        if outputFolder is not None:
            with open(outputFolder + "/tree_rules.txt", 'w+') as f:
                f.write(tree_rules)
                f.close()
        else:
            print(tree_rules)

        # All done!
        return tree

    def output(self, outputFolder):
        print("Output Decision Tree")
        #todo: this is probably a worth while member


    def test(self):
        y_pred = self.__dtree.predict(self.dataSource.x_test)

        accuracy = sklearn.metrics.accuracy_score(self.dataSource.y_test, y_pred)
        print(f'Accuracy: {accuracy}')
        print(sklearn.metrics.classification_report(self.dataSource.y_test, y_pred))
        # cross_val_score(self.__dtreecv=10)
