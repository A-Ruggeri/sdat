
class conColors:
    RED    = '\033[91m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    BLUE   = '\033[94m'
    HEADER = '\033[95m'
    CYAN   = '\033[96m'
    WHITE  = '\033[97m'

    ENDC   = '\033[0m'
    BOLD   = '\033[1m'
    UNDERLINE = '\033[4m'


def printError(errorString : str):
    print(conColors.RED + "ERROR: " + errorString + conColors.ENDC)

def printWarning(warningString : str):
    print(conColors.YELLOW + "WARN: " + warningString + conColors.ENDC)

def printDebug(debugString : str):
    print(conColors.BLUE + "DEBUG: " + debugString + conColors.ENDC)

def printInfo(infoString : str):
    print(conColors.BOLD + conColors.CYAN + infoString + conColors.ENDC)

def printStd(stdString : str):
    print(stdString)