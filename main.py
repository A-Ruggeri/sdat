#!/usr/bin/python3

# Imports
import sys
import os
from compute.helper.loging import printError, printInfo, printStd
from jsonParser import jsonParser
from textParser import textParser


def pathCheck(path):
    if os.path.isfile(path):
        return path

    relPath = os.getcwd() + path
    if os.path.isfile(relPath):
        return relPath

    return False


# ------------------------------------------------------------------
# Script Start
# ------------------------------------------------------------------
if len(sys.argv) != 2:
    printError("Need configuration file")
    exit(-1)


# ------------------------------------------------------------------
filePath = sys.argv[1]
printInfo(f'Running: {filePath}')

# Check if file exists
pathReturn = pathCheck(filePath)
if pathReturn is False:
    printError(f"File not found")
    exit(-1)

# Check if absolute or relative
if pathReturn is not filePath:
    filePath = pathReturn
    printStd(f"Path Switched: {filePath}")

# if the file is JSON
if filePath.endswith(".json"):
    printStd(f'json File: {filePath}')
    jsonParser(filePath)

# if the file
elif filePath.endswith(".txt"):
    printStd(f'Text File: {filePath}')
    textParser(filePath)

else:
    printError("File type not supported")
    exit(-1)

# Everything looks good, return and exit
printInfo("~Et Fin~")
exit(0)