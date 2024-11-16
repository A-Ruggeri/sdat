# import decisionTree


def textParser(filePath):
    cmdFile = open(filePath, 'r')  # todo: test for file existance
    lines = cmdFile.readlines()

    # Create decisionTree
    # dt = decisionTree.DecisionTree()

    databaseLoad = dict()

    for line in lines:
        cmds = line.replace('\n', '').split(' ')

        # it's Binary
        # ----------------------------------------------------------
        if (len(cmds) == 3) or (len(cmds) == 4):  # hack allow 4 and just drop the 'CAT'
            print('temp')
            # dt.addIndependantVar(cmds[0], cmds[1], cmds[2])
            # fieldpar = (cmds[1], cmds[2])
            # collectionFieldList = [fieldpar]
            #
            # if cmds[0] in databaseLoad:
            #     databaseLoad[cmds[0]] += collectionFieldList
            # else:
            #     databaseLoad[cmds[0]] = collectionFieldList



        # Else, ignore it
        # ----------------------------------------------------------
        else:
            print("reject current line")

    # All done, it's more fun to compute
    # dt.calculate()
    return True