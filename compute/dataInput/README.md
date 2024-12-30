# Data Input
Classes which handle the reading of data into the code base to be used by computation classes.

## Data Input Types
The following are the classes setup for data input

| Name                 | Description                          |
|-------------------   | --------------------                 |
| dataCsvFile          | data source is a CSV file            |
| dataMongoDb          | data source is Mongo DB              | 

### dataObjFactory.py
This file is singleton, which contains an instance of whichever data input type is configured.