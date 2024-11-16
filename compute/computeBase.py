#imports

class computeBase():
    """
    base class for compute classes
    """
    def __init__(self, **kwargs):
        print("base")

    def compute(self, outputDirectory: str) -> bool:
        print("it's more fun to compute")
        return False