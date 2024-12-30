#imports
import compute.computeBase
import pandas
import numpy
import statsmodels
from compute.loging import printInfo


class LogisticRegression(compute.computeBase.computeBase):

    def __init__(self, **kwargs):
        super(LogisticRegression, self).__init__()

        printInfo("Logistic Regression")

        # Update default class values with ones from JSON
        self.__dict__.update(kwargs)


    def __str__(self):
        # Clean this up later
        return f"Logistic Regression: {self.__dict__}"



    # ------------------------------------------------------------------
    # __createFormulaString
    # ------------------------------------------------------------------
    def __createFormulaString(self):

        # Form the formula string
        blrFormulaStr = f'PDC_NON_ADHR ~ '
        for colName in self.__dataFrame.columns[1:]:
            # Check if this column is catagorical
            if self._QueryMongo__dataFrame[colName].dtype.name == "category":
                # get the mode
                mode = self.__dataFrame[colName].mode(dropna=True)
                blrFormulaStr += f'C({colName}, Treatment(reference=\"{mode[0]}\")) + '
            else:
                blrFormulaStr += f'{colName} + '

        return blrFormulaStr[:-3]  # trailing '+ ' can be cut via substring


    def calculate(self):
        print(".......................................................")
        print("\tComputing...BEEP BEEP BEEP")

        blrFormulaStr = self.__createFormulaString()
        print(f'\tComputing: {blrFormulaStr}')

        # Calculate BLR
        blrResult = statsmodels.formula.api.logit(formula=blrFormulaStr, data=self.__dataFrame).fit()
        print(blrResult.summary())

        # Calculate Odds Ratio and Confidence Interval
        oddsDf = pandas.DataFrame()
        oddsDf['odds_ratio'] = numpy.exp(blrResult.params)
        oddsDf['p_value'] = blrResult.pvalues
        oddsDf[['ci_ll', 'ci_up']] = numpy.exp(numpy.array(blrResult.conf_int(), dtype=numpy.float128))
        oddsDf.drop('Intercept', inplace=True)

        # names = list()
        # for idx in oddsDf.index:
        #     columnName = self.__searchDict[idx]
        #     searchTerm = idx.split('_')[-1]
        #     fieldName = self.__dnh.getName(columnName, searchTerm)
        #     names.append(fieldName)

        # oddsDf['field_name'] = names
        # oddsDf['odds_str'] = ""
        # for index in oddsDf.index:
        #     oddsDf._set_value(index, 'odds_str', f'({round(oddsDf.loc[index, "ci_ll"],2)}, {round(oddsDf.loc[index, "ci_up"],2)})')

        names = list()
        values = list()
        fieldName = list()
        groupNames = list()
        for fullName in oddsDf.index:
            fullName = str(fullName)
            name = fullName[2:fullName.find(',')]
            value = fullName[fullName.find('.') + 1:-1]
            groupNames.append(self.__dnh.getGroup(name, value))
            tempFieldName = self.__dnh.getName(name, value)
            if self.__dnh.getGroup(name, value) != "":
                    tempFieldName = str(f'    {tempFieldName}')
            fieldName.append(tempFieldName)
            names.append(name)
            values.append(value)

        oddsDf['field_name'] = fieldName
        oddsDf['name'] = names
        oddsDf['value'] = values
        oddsDf['group_name'] = groupNames
        #
        #
        count = list()
        for indx in oddsDf.index:
            field = oddsDf.loc[indx, 'name']
            value = oddsDf.loc[indx, 'value']
            catInfo = self.__dataFrame[field].value_counts(dropna=True)
            count.append(catInfo[value])
        #     # oddsDf._set_value(indx, 'N', catInfo.loc[])
        oddsDf['n'] = count


        # Move field_name to be first column, makes manual edits easier
        first_column = oddsDf.pop('field_name')
        oddsDf.insert(0, 'field_name', first_column)

        # Arrange all the grouped fields togther
        oddsDf.sort_values(by=['group_name'], inplace= True)

        # Insert empy rows For 'header' sections
        pre_indx = oddsDf.index[-1]
        prev_group = oddsDf['group_name'].iloc[-1]
        print(len(oddsDf.index.values))
        for index in reversed(oddsDf.index):
            cur_group = oddsDf.loc[index, 'group_name']

            if cur_group != prev_group:
                header = pandas.DataFrame({'field_name': [prev_group], 'group_name': [prev_group]})
                oddsDfTop = oddsDf[:index]
                oddsDfBtm = oddsDf[pre_indx:]
                oddsDf = pandas.concat([oddsDfTop, header])
                oddsDf = pandas.concat([oddsDf, oddsDfBtm])
                print(len(oddsDf.index.values))
                # pandas.concat([df.iloc[:idx_pos], new_row, df.iloc[idx_pos:]])
            pre_indx = index
            prev_group = cur_group

        # Add header to top of odds data frame
        header = pandas.DataFrame({'field_name': [oddsDf['group_name'].iloc[0]], 'group_name': [oddsDf['group_name'].iloc[0]]})
        oddsDf = pandas.concat([header, oddsDf])

        # drop the ugly index names too
        oddsDf.reset_index(drop=True, inplace=True)




        print(oddsDf)
        oddsDf.to_csv('blrInfo.csv')
        return oddsDf


    def computeDataStats(self):
        print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_")
        print("\tGetting Data Stats on data")

        # We will return a dict of 'field' : DF:stats info
        statsDfDict = dict()
        totalCount = len(self.__dataFrame.index)

        for columnName in self.__dataFrame.columns[1:]:
            # Get a count of all valid (non-nan) data in the column
            missCount = self.__dataFrame[columnName].isna().sum()
            validCount = totalCount - missCount
            catInfo = self.__dataFrame[columnName].value_counts(dropna=True)
            statsDf = pandas.DataFrame(catInfo)
            statsDf["percValid"] = -1.1
            statsDf["percTotal"] = -1.1
            statsDf["fieldName"] = ""
            for catName in catInfo.index:
                perc = (catInfo[catName] / validCount) * 100
                statsDf._set_value(catName, "percValid", perc)

                percTotal = (catInfo[catName] / totalCount) * 100
                statsDf._set_value(catName, "percTotal", percTotal)

                fieldName = self.__dnh.getName(columnName, catName)
                statsDf._set_value(catName, "fieldName", fieldName)
                # print(f'\t{str(catName)}\t{catInfo[catName]:,}\t{round(perc,2)}')


            statsDf.loc['Valid_Data'] = [validCount, (validCount / totalCount) * 100, 0, ""]
            statsDf.loc['M+O_Data']   = [missCount,  (missCount / totalCount) * 100, 0, ""]
            print(statsDf)

            # Add to the dictionary
            statsDfDict[columnName] = statsDf
            print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")
        return statsDfDict



