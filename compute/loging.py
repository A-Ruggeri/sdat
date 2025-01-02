
class conColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printError(errorString : str):
    print(conColors.RED + "ERROR: " + errorString + conColors.ENDC)

def printInfo(infoString : str):
    print(conColors.BOLD + conColors.CYAN + infoString + conColors.ENDC)