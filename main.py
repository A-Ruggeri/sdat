#!/usr/bin/python3

# Imports
import sys
import os
from jsonParser import jsonParser
from textParser import textParser

# ------------------------------------------------------------------
# Script Start
# ------------------------------------------------------------------
if len(sys.argv) != 2:
    print("Need: <file>")
    exit(-1)


# ------------------------------------------------------------------
filePath = sys.argv[1]
print(f'Running: {filePath}')

# Check if file exists
if not os.path.isfile(filePath):
    print("File not found")
    exit(-1)

# if the file is JSON
if filePath.endswith(".json"):
    print(f'json File: {filePath}')
    jsonParser(filePath)

# if the file
elif filePath.endswith(".txt"):
    print(f'Text File: {filePath}')
    textParser(filePath)

else:
    print("File type not supported")
    exit(-1)

# Everything looks good, return and exit
print("~Et Fin~")
exit(0)