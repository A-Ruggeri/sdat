
# IMPORTS
import pandas



class dataNameHelper:
    def __init__(self):
        self.__csvFile = pandas.read_csv("fieldNameMap.csv")
        self.__csvFile.set_index(['Database Field', 'Field Value'], inplace=True)

    def getName(self, fieldName, fieldValue):
        # force lookup to be lowercase case
        fieldValue = str(fieldValue).lower()
        name = str(f'{fieldName}_{fieldValue}')
        if (fieldName, fieldValue) in self.__csvFile.index:
            name = self.__csvFile.loc[(fieldName, fieldValue)]['Printed Name']
        else:
            print(f'Field Error: {fieldName} with {fieldValue} not found')
        return name

    def getGroup(self, fieldName, fieldValue):
        fieldValue = str(fieldValue).lower()
        groupName = fieldName
        if (fieldName, fieldValue) in self.__csvFile.index:
            groupName = self.__csvFile.loc[(fieldName, fieldValue)]['Group']
        else:
            print(f'Group Error: {fieldName} with {fieldValue} not found')
        return groupName