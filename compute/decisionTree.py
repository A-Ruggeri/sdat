#import
import compute.computeBase
import pandas
import sklearn
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt


class DecisionTree(compute.computeBase.computeBase):
    def __init__(self, **kwargs):
        super(DecisionTree, self).__init__()

        print("Decision Tree")

        # Default tuning parameters
        self.maxTreeDepth = 3
        self.minSplitNum = 2
        self.maxFeatures = 1
        self.randomSeed = None

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

        X = self.dataSource.dataFrame[features]
        y = self.dataSource.dataFrame['PDC_NON_ADHR']


        # Create the model
        self.__dtree = DecisionTreeClassifier(max_depth = self.maxTreeDepth,
                                       min_samples_split = self.minSplitNum,
                                       max_features = self.maxFeatures,
                                       random_state = self.randomSeed)
        self.__dtree = self.__dtree.fit(X, y)


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


    def test(self):
        y_pred = self.__dtree.predict(self.dataSource.X_test)

        accuracy = sklearn.metrics.accuracy_score(self.dataSource.y_test, y_pred)
        print(f'Accuracy: {accuracy}')
        print(sklearn.metrics.classification_report(self.dataSource.y_test, y_pred))
        # cross_val_score(self.__dtreecv=10)
