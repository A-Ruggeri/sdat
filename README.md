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
  "dataSource": {
    "mongoDb": {
      "ip": "localhost",
      "port": "27017"
    }
  },
  "decisionTree": {
    "maxTreeDepth": 3,
    "maxFeatures": 2
  }
}
```
## dataSource
Sets where the data will be pulled from

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

## Computation Method To Run
The next element is for a computation to run with the provided data based on the datasource.


### Decision Tree
Arguments depend on the 

| Name         | Value   | Description                      |
|--------------|---------|----------------------------------|
| maxTreeDepth | int     | Tree depth                       |
| maxFeatures  | int     | Max number of feature to be used |

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