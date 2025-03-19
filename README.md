# SEER Database Analysis Tools

![GitHub repo size](https://img.shields.io/github/repo-size/A-Ruggeri/sdat)


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
  "dataSource": {
    "mongoDb": {
      "ip": "localhost",
      "port": "27017"
    },
    "targetName" : "IdValue"
  },
  "decisionTree": {
    "maxTreeDepth": 3,
    "maxFeatures": 2
  }
}
```
## dataSource
Contains one of the suboptions listed below, to select where the data will come from.

| Name        | Value        | Description                                                              |
|-------------|--------------|--------------------------------------------------------------------------|
| targetName  | str          | Name of target feature loaded from data                                  |
| data Source | json Element | Element with configure info for loading data ('MongoDb', 'csvFile', ect) |


### mongoDb
pull data from mongo db

| Name | Value | Description                                    |
|------|-------|------------------------------------------------|
| ip   | str   | string to the ip where the Mongo DB is running |
| port | int   | port number for mongo DB server                |


### csvFile
pull data from csv file

| Name     | Value | Description      |
|----------|-------|------------------|
| filePath | str   | Path to CSV file |

### data

### training
| Name       | Value | Description                                        |
|------------|-------|----------------------------------------------------|
| split      | int   | Percentage of data to allocate for testing         |
| randomSeed | int   | Provide fixed seed value for deterministic results |


## Computation Method To Run
The next element is for a computation to run with the provided data based on the datasource.


### Decision Tree
Arguments depend on the 

| Name         | Value        | Description                                                                    |
|--------------|--------------|--------------------------------------------------------------------------------|
| maxTreeDepth | int \ array  | Tree depth                                                                     |
| maxFeatures  | int \ array  | Max number of feature to be used                                               |
| minSplitNum  | int \ array  | Minium Split Value                                                             |
| randomSeed   | int          | Provide fixed seed value for deterministic results                             |
| gridSearch   | int \ bool   | When set to '1' or 'True', will enable gride search with the provided array values |

NOTE: When gridSearch is enabled, all DT arguments listed as such need to be array values (even if they are singular)

### Logistic Regression

## Output
Sets the location and parameters for where the resulting output files should be saved

| Name       | Value  | Description                                        |
|------------|--------|----------------------------------------------------|
| saveJson   | 0,1    | Save the JSON file used alone with the output data |
| directory  | text   | Directory location to save output data             |
| timestamp  | 0,1    | Append timestamp to output directory name          | 

## Dependencies
The follow is a list of dependencies used within the compute pacakge
* sklearn
* numpy
* pandas

## Comments

## Other