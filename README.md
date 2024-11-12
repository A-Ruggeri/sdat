# SEER Database Analysis Tools


## Overview
SEER database analysis toolkit written in python3. The tool is command line driven with the configuration infomation provided via arguments and config files. The tool has been primariy tested on *nix based systems with data being stored in mongodb.

## Usage

`$ ./main.py <arguments>`

or

`$ python3 main.py <arguments>`

### JSON Config File
The following is an example of a json configuration file used for tuning a decision tree.

```json
{
  "mongo": {
    "ip": "localhost",
    "port": "27017"
  },
  "decisionTree": {
    "maxTreeDepth": 3,
    "maxFeatures": 2
  }
}
```

## Decision Tree
Arguments depend on the 


## Logistic Regression

## Output
Sets the location and parameters for where the resulting output files should be saved

| Name       | option | Description                                        |
|------------|--------|----------------------------------------------------|
| saveJson   | 0,1    | Save the JSON file used alone with the output data |
| directory  | text   | Directory location to save output data             |
| timestamp  | 0,1    | Append timestamp to output directory name          | 

## Dependencies
some dependencies you can avoid 
* Python 3
* sklearn
* numpy
* pandas

## Comments

## Other