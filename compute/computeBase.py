#imports
import compute.dataInput.dataObjFactory
from compute.helper.loging import printInfo


class computeBase():
    """
    base class for compute classes
    """
    def __init__(self, **kwargs):

        # Get datasource
        self.dataSource = None

        dof = compute.dataInput.dataObjFactory.dataObjFactory()
        if dof.isInitiated() is False:
            print("No data source set up, can not calculate decision tree.")
            return

        self.dataSource = dof.getDataInputSource()


    def __str__(self):
        return f"{self.__class__.__name__}"


    def compute(self, outputDirectory: str):
        printInfo("it's more fun to compute")


    def test(self):
        printInfo("Testing Model")