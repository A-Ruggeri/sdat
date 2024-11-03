#imports

import sys
import json

def jsonParser(filename):
    fs = open(filename, 'r')
    data = json.load(fs)

    return False