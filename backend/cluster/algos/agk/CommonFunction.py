# -*- coding: utf-8 -*-
import json
import sys

import numpy as np
from ge import DeepWalk, LINE, Node2Vec, Struc2Vec, SDNE
import networkx as nx
from sklearn.cluster import AgglomerativeClustering, DBSCAN, SpectralClustering

from cluster.algos.agk.AGK import AGK


def makeGraphInAion(variables, cells, useList, dictFileLabel):
    dict1 = {}
    for variableNum in range(len(variables)):
        if variableNum not in useList:
            continue
        variableFile = judgeWhichFileInAion(variables[variableNum])
        if variableFile == '':
            continue
        if variableFile not in dict1.keys():
            dict1[variableFile] = []
        dict1[variableFile].append(variableNum)

    graph = []
    for cellNum in range(len(cells)):
        src = cells[cellNum]['src']
        dest = cells[cellNum]['dest']
        if src not in useList or dest not in useList:
            continue
        srcKey = judgeWhichKey(dict1, src)
        destKey = judgeWhichKey(dict1, dest)
        if srcKey is None or destKey is None or srcKey == destKey:
            continue
        srcLabel = dictFileLabel[srcKey]
        destLabel = dictFileLabel[destKey]
        if [srcLabel, destLabel] not in graph:
            graph.append([srcLabel, destLabel])
    return graph


def generateUseList(startName, variables):
    usefulList = []
    for i in range(len(variables)):
        if variables[i].startswith(startName):
            usefulList.append(i)
    return usefulList


def generateFileLabelInAion(variables):
    dictFileLabel = {}
    fileIndex = 0
    for variableNum in range(len(variables)):
        variableFilename = judgeWhichFileInAion(variables[variableNum])
        if variableFilename not in dictFileLabel.keys() and variableFilename != '':
            dictFileLabel[variableFilename] = fileIndex
            fileIndex += 1
    return dictFileLabel


def generateLabelWithoutReductionDimInAion(graph, variables, usefulList, dictFileLabel, GraphEmbeddingIndex, clusters,
                                           linkage):
    global modelTemp
    if GraphEmbeddingIndex == 0:
        modelTemp = Struc2Vec(graph, 10, 80, workers=4, verbose=40, )
        modelTemp.train(window_size=5, iter=3)
    elif GraphEmbeddingIndex == 1:
        modelTemp = DeepWalk(graph, walk_length=10, num_walks=80, workers=4)
        modelTemp.train(window_size=5, iter=3)
    elif GraphEmbeddingIndex == 2:
        modelTemp = LINE(graph, embedding_size=128, order='second')
        modelTemp.train(batch_size=1024, epochs=50, verbose=2)
    elif GraphEmbeddingIndex == 3:
        modelTemp = Node2Vec(graph, walk_length=10, num_walks=80, p=0.5, q=5, workers=1)
        modelTemp.train(window_size=5, iter=3)
    elif GraphEmbeddingIndex == 4:
        modelTemp = SDNE(graph, hidden_size=[256, 128])
        modelTemp.train(batch_size=3000, epochs=40, verbose=2)
    embeddingsTemp = modelTemp.get_embeddings()

    embeddingsKeyTemp = []
    for i in embeddingsTemp:
        embeddingsKeyTemp.append(int(i))
    embeddingsKeyTemp.sort()
    embListTemp = []
    for item in embeddingsKeyTemp:
        embListTemp.append(embeddingsTemp[str(item)])

    # AGK
    # embListTemp = np.array(embListTemp)
    # label_pred = UseInWeka.AGK(embListTemp, clusters)

    # AgglomerativeClustering
    clustering = AgglomerativeClustering(n_clusters=clusters, linkage=linkage).fit(embListTemp)
    label_pred = clustering.labels_

    # KMeans
    # clustering = KMeans(n_clusters=clusters).fit(embListTemp)
    # label_pred = clustering.labels_

    # SKM
    # embListTemp = np.array(embListTemp)
    # label_pred = SKM.SMKM(embListTemp, clusters, 1)

    # agglomerative
    # agglomerative_instance = agglomerative(embListTemp, 10, type_link.SINGLE_LINK, ccore=True)
    # agglomerative_instance.process()
    # label_pred = agglomerative_instance.get_clusters()

    # DBSCAN
    # db = DBSCAN(eps=3, min_samples=10).fit(embListTemp)
    # label_pred = db.labels_

    # SpectralClustering
    # clustering = SpectralClustering(n_clusters=clusters, assign_labels='discretize', random_state=0).fit(embListTemp)
    # label_pred = clustering.labels_

    print(label_pred)

    dictClusterRes = {}
    for embeddingNum in range(len(embeddingsKeyTemp)):
        fileName = findFilename(embeddingsKeyTemp[embeddingNum], dictFileLabel)
        dictClusterRes[fileName] = label_pred[embeddingNum]

    clusterResultLabel = [[] for num in range(clusters)]
    for variableNum in range(len(variables)):
        if variableNum not in usefulList:
            continue
        fileNameInSource = judgeWhichFileInAion(variables[variableNum])
        if fileNameInSource != '' and fileNameInSource in dictClusterRes.keys():
            clusterResultLabel[dictClusterRes[fileNameInSource]].append(variables[variableNum])
    return clusterResultLabel, embListTemp, label_pred, embeddingsKeyTemp


def writeResult(filename, clusterResult):
    with open(filename, "w") as f:
        for i in range(len(clusterResult)):
            for item in clusterResult[i]:
                temp = 'contain ' + str(i) + ' ' + str(item) + '\n'
                f.writelines(temp)


def generateTheGroundTruth(variable, clusterNum):
    trueResult = [[] for i in range(clusterNum)]
    index = -1
    for variableIndex in range(len(variable)):
        if variable[variableIndex] == 'module-info':
            index += 1
        if variable[variableIndex].startswith('org.aion.') and JudgeToFile(variable[variableIndex]):
            trueResult[index].append(variable[variableIndex])
    return trueResult


def JudgeToFile(filename):
    haveHigh = False
    for fileIndex in range(len(filename)):
        if 'A' <= filename[fileIndex] <= 'Z':
            for extendIndex in range(fileIndex + 1, len(filename)):
                if filename[extendIndex] == '.':
                    haveHigh = True
                    break
    return haveHigh


def WriteMojofmFileReal(clusterResult, filePath):
    with open(filePath, "w") as f:
        for i in range(len(clusterResult)):
            for item in clusterResult[i]:
                temp = 'contain ' + str(i) + ' ' + str(item) + '\n'
                f.writelines(temp)


def generateTheGroundTruthInWebfx(variable, clusterNum, useList):
    trueResult = [[] for i in range(clusterNum)]
    index = 0
    for variableIndex in range(len(variable)):
        if variable[variableIndex] == 'module-info':
            index += 1
        if variableIndex in useList and JudgeToFile(variable[variableIndex]):
            trueResult[index].append(variable[variableIndex])
    return trueResult


def WriteInputGraphWhenHistory(cells, filename):
    with open(filename, "w") as f:
        for each in cells:
            temp = str(each['src']) + " " + str(each['dest']) + '\n'
            f.writelines(temp)


def generateLabelWithoutReductionDim(graph, variables, GraphEmbeddingIndex=0, clusters=16, linkage='complete'):
    global modelTemp
    if GraphEmbeddingIndex == 0:
        modelTemp = Struc2Vec(graph, 10, 80, workers=4, verbose=40, )
        modelTemp.train(window_size=5, iter=3)
    elif GraphEmbeddingIndex == 1:
        modelTemp = DeepWalk(graph, walk_length=10, num_walks=80, workers=1)
        modelTemp.train(window_size=5, iter=3)
    elif GraphEmbeddingIndex == 2:
        modelTemp = LINE(graph, embedding_size=128, order='second')
        modelTemp.train(batch_size=1024, epochs=50, verbose=2)
    elif GraphEmbeddingIndex == 3:
        modelTemp = Node2Vec(graph, walk_length=10, num_walks=80, p=0.25, q=4, workers=1)
        modelTemp.train(window_size=5, iter=3)
    elif GraphEmbeddingIndex == 4:
        modelTemp = SDNE(graph, hidden_size=[256, 128])
        modelTemp.train(batch_size=3000, epochs=40, verbose=2)
    embeddingsTemp = modelTemp.get_embeddings()

    embeddingsKeyTemp = []
    for i in embeddingsTemp:
        embeddingsKeyTemp.append(int(i))
    embeddingsKeyTemp.sort()
    embListTemp = []
    for item in embeddingsKeyTemp:
        embListTemp.append(embeddingsTemp[str(item)])

    # clustering = AgglomerativeClustering(n_clusters=clusters, linkage=linkage).fit(embListTemp)
    # label_pred = clustering.labels_

    # AGK
    embListTemp = np.array(embListTemp)
    label_pred = AGK(embListTemp, clusters)

    clusterResultLabel = []

    for num in range(clusters):
        temp = []
        for i in range(len(label_pred)):
            if label_pred[i] == num:
                temp.append(variables[embeddingsKeyTemp[i]])
        clusterResultLabel.append(temp)
    return clusterResultLabel


def findFileRealIndex(variable, filename):
    modelinfoIndex = -1
    for varIndex in range(len(variable)):
        if variable[varIndex] == 'module-info':
            modelinfoIndex += 1
        var = variable[varIndex]
        if var.find(filename) != -1:
            return modelinfoIndex


################################
# mainMethod function

def LoadJsonFile(filename):
    data = json.load(open(filename))
    cells = data['cells']
    variables = data['variables']
    return data, cells, variables


def generateUseListInDifSw(variables, swName):
    usefulList = []
    global startName
    if swName == 'Aion':
        startName = 'org.aion.'
    elif swName == 'Junit':
        startName = 'org.junit.'
    elif swName == 'AndroidCore':
        startName = 'android.'
    elif swName.startswith('NewForm'):
        startName = ''
    else:
        sys.exit("软件名不存在")

    for i in range(len(variables)):
        if variables[i].startswith(startName):
            usefulList.append(i)
    return usefulList


def generateFileLabel(variables, swName):
    global variableFilename
    dictFileLabel = {}
    fileIndex = 0
    for variableNum in range(len(variables)):
        if swName == 'Aion':
            variableFilename = judgeWhichFileInAion(variables[variableNum])
        elif swName == 'Junit':
            variableFilename = judgeWhichFileInJunit(variables[variableNum])
        elif swName == 'AndroidCore':
            variableFilename = judgeWhichFileInAion(variables[variableNum])
        elif swName.startswith('NewForm'):
            variableFilename = judgeWhichFileInAion(variables[variableNum])
        else:
            sys.exit("软件名不存在")

        if variableFilename not in dictFileLabel.keys() and variableFilename != '':
            dictFileLabel[variableFilename] = fileIndex
            fileIndex += 1
    return dictFileLabel


def makeGraph(variables, cells, useList, dictFileLabel, swName):
    global variableFile
    dict1 = {}
    for variableNum in range(len(variables)):
        if variableNum not in useList:
            continue

        if swName == 'Aion':
            variableFile = judgeWhichFileInAion(variables[variableNum])
        elif swName == 'Junit':
            variableFile = judgeWhichFileInJunit(variables[variableNum])
        elif swName == 'AndroidCore':
            variableFile = judgeWhichFileInAion(variables[variableNum])
        elif swName.startswith('NewForm'):
            variableFile = judgeWhichFileInAion(variables[variableNum])
        else:
            sys.exit("软件名不存在")

        if variableFile == '':
            continue
        if variableFile not in dict1.keys():
            dict1[variableFile] = []
        dict1[variableFile].append(variableNum)

    graph = []
    important = ['Call', 'Parameter', 'Inherit', 'Call non-dynamic', 'Implement']
    for cellNum in range(len(cells)):
        src = cells[cellNum]['src']
        dest = cells[cellNum]['dest']
        valueKeyTemp = list(cells[cellNum]['values'].keys())
        valueKey = valueKeyTemp[0]
        weight = 1
        if valueKey in important:
            weight = 2
        if src not in useList or dest not in useList:
            continue
        srcKey = judgeWhichKey(dict1, src)
        destKey = judgeWhichKey(dict1, dest)
        if srcKey is None or destKey is None or srcKey == destKey:
            continue
        srcLabel = dictFileLabel[srcKey]
        destLabel = dictFileLabel[destKey]
        if [srcLabel, destLabel] not in graph:
            graph.append([srcLabel, destLabel, int(weight)])
    return graph


def writeInputGraph(graph, filePath):
    with open(filePath, "w") as f:
        for each in graph:
            temp = str(each[0]) + " " + str(each[1]) + " " + str(each[2]) + '\n'
            f.writelines(temp)


def generateLabel(graph, variables, usefulList, dictFileLabel, GraphEmbeddingIndex, clusters, clusterAlgorithm, swName):
    global modelTemp, label_pred, fileNameInSource
    if GraphEmbeddingIndex == 0:
        modelTemp = Struc2Vec(graph, 10, 80, workers=4, verbose=40, )
        modelTemp.train(window_size=5, iter=3)
    elif GraphEmbeddingIndex == 1:
        modelTemp = DeepWalk(graph, walk_length=10, num_walks=80, workers=4)
        modelTemp.train(window_size=5, iter=3)
    elif GraphEmbeddingIndex == 2:
        modelTemp = LINE(graph, embedding_size=128, order='second')
        modelTemp.train(batch_size=1024, epochs=50, verbose=2)
    elif GraphEmbeddingIndex == 3:
        modelTemp = Node2Vec(graph, walk_length=10, num_walks=80, p=0.5, q=5, workers=1)
        modelTemp.train(window_size=5, iter=3)
    elif GraphEmbeddingIndex == 4:
        modelTemp = SDNE(graph, hidden_size=[256, 128])
        modelTemp.train(batch_size=3000, epochs=40, verbose=2)
    embeddingsTemp = modelTemp.get_embeddings()

    embeddingsKeyTemp = []
    for i in embeddingsTemp:
        embeddingsKeyTemp.append(int(i))
    embeddingsKeyTemp.sort()
    embListTemp = []
    for item in embeddingsKeyTemp:
        embListTemp.append(embeddingsTemp[str(item)])

    if clusterAlgorithm == 'AGK':
        # AGK
        embListTemp = np.array(embListTemp)
        label_pred = AGK(embListTemp, clusters)
    # elif clusterAlgorithm == 'SKM':
    #     # SKM
    #     embListTemp = np.array(embListTemp)
    #     label_pred = SKMAlg.SMKM(embListTemp, clusters, 1)
    elif clusterAlgorithm == 'DBSCAN':
        # DBSCAN
        db = DBSCAN(eps=3, min_samples=10).fit(embListTemp)
        label_pred = db.labels_
    elif clusterAlgorithm == 'SpectralClustering':
        # SpectralClustering
        clustering = SpectralClustering(n_clusters=clusters, assign_labels='discretize', random_state=0).fit(
            embListTemp)
        label_pred = clustering.labels_
    elif clusterAlgorithm == 'ward' or clusterAlgorithm == 'single' or clusterAlgorithm == 'average' or clusterAlgorithm == 'complete':
        # AgglomerativeClustering
        clustering = AgglomerativeClustering(n_clusters=clusters, linkage=clusterAlgorithm).fit(embListTemp)
        label_pred = clustering.labels_

    # print(label_pred)

    dictClusterRes = {}
    for embeddingNum in range(len(embeddingsKeyTemp)):
        fileName = findFilename(embeddingsKeyTemp[embeddingNum], dictFileLabel)
        dictClusterRes[fileName] = label_pred[embeddingNum]

    clusterResultLabel = [[] for num in range(clusters)]
    for variableNum in range(len(variables)):
        if variableNum not in usefulList:
            continue
        if swName == 'Aion':
            fileNameInSource = judgeWhichFileInAion(variables[variableNum])
        elif swName == 'Junit':
            fileNameInSource = judgeWhichFileInJunit(variables[variableNum])
        elif swName == 'AndroidCore':
            fileNameInSource = judgeWhichFileInAion(variables[variableNum])
        elif swName.startswith('NewForm'):
            fileNameInSource = judgeWhichFileInAion(variables[variableNum])
        else:
            sys.exit("软件名不存在")

        if fileNameInSource != '' and fileNameInSource in dictClusterRes.keys():
            clusterResultLabel[dictClusterRes[fileNameInSource]].append(variables[variableNum])
    return clusterResultLabel, embListTemp, label_pred, embeddingsKeyTemp


def writePreResultMojoFM(filePath, clusterResult):
    with open(filePath, "w", encoding='utf-8') as f:
        for i in range(len(clusterResult)):
            for item in clusterResult[i]:
                temp = 'contain ' + str(i) + ' ' + str(item) + '\n'
                f.writelines(temp)


def getRealColor(variable):
    colorDict = {}
    colorIndex = 0
    for variableIndex in range(len(variable)):
        colorDict[variable[variableIndex]] = colorIndex
        if variable[variableIndex] == "module-info":
            colorIndex += 1
    return colorDict


def writeResultMojoFMReal(colorDict, filePath):
    with open(filePath, "w", encoding='utf-8') as f:
        for item in colorDict.keys():
            if item != '':
                temp = 'contain ' + str(colorDict[item]) + ' ' + str(item) + '\n'
            f.writelines(temp)


def judgeWhichFileInAion(variable):
    left = -1
    right = -1
    for variableIndex in range(len(variable)):
        if 'A' <= variable[variableIndex] <= 'Z' and left == -1:
            left = variableIndex
            for j in range(variableIndex + 1, len(variable)):
                if variable[j] == '.':
                    right = j
                    break
            break
    if right == -1:
        return ''
    return variable[left:right]


def judgeWhichFileInJunit(variable):
    left = -1
    right = -1
    passOne = 3
    for varNum in range(len(variable)):
        if variable[varNum] == '.':
            if passOne != 0:
                passOne -= 1
            else:
                if left == -1:
                    left = varNum + 1
                else:
                    right = varNum
                    break
    if right == -1:
        return ''
    return variable[left:right]


def findFilename(fileIndex, dictFileLabel):
    for file in dictFileLabel.keys():
        if dictFileLabel[file] == fileIndex:
            return file
    return None


def judgeWhichKey(dict1, value):
    for itemKey in dict1.keys():
        for itemValue in dict1[itemKey]:
            if itemValue == value:
                return itemKey
    return None


################################


def mainMethod(SoftwareName, jsonFileName, AssociationNetworkName, GraphEmbeddingAlgorithm, ClusterAlgorithm,
               ClusterNum):
    data_construct, cells_construct, variables_construct = LoadJsonFile(jsonFileName)

    # for android software
    if SoftwareName.startswith('NewForm'):
        variables = []
        for item in variables_construct:
            variables.append(item['qualifiedName'])
        variables_construct = variables

    useList = generateUseListInDifSw(variables=variables_construct, swName=SoftwareName)
    dictFileLabel = generateFileLabel(variables=variables_construct, swName=SoftwareName)

    graphManual = makeGraph(variables=variables_construct,
                            cells=cells_construct,
                            useList=useList,
                            dictFileLabel=dictFileLabel,
                            swName=SoftwareName)

    inputFilePath = r'.\cluster\algos\agk\data\txtFile\inputFiles' + '\\' + SoftwareName + '-' + AssociationNetworkName + '-Input.txt'
    writeInputGraph(graphManual, inputFilePath)

    Graph = nx.read_edgelist(inputFilePath, create_using=nx.DiGraph(), nodetype=None, data=[('weight', int)])

    GraphEmbeddingIndex = -1
    if GraphEmbeddingAlgorithm == 'Struc2Vec':
        GraphEmbeddingIndex = 0
    elif GraphEmbeddingAlgorithm == 'DeepWalk':
        GraphEmbeddingIndex = 1
    elif GraphEmbeddingAlgorithm == 'Node2Vec':
        GraphEmbeddingIndex = 3

    clusterResult, embListTemp1, label_pred1, embeddingsKeyTemp1 \
        = generateLabel(graph=Graph,
                        variables=variables_construct,
                        usefulList=useList,
                        dictFileLabel=dictFileLabel,
                        GraphEmbeddingIndex=GraphEmbeddingIndex,
                        clusters=int(ClusterNum),
                        clusterAlgorithm=ClusterAlgorithm,
                        swName=SoftwareName)

    mojoFMResPreFilePath = r'.\cluster\algos\agk\data\txtFile\mojoFMFiles' + '\\' + SoftwareName + '-' + GraphEmbeddingAlgorithm + '-' + ClusterAlgorithm + '-' + 'MojoFM.txt'
    writePreResultMojoFM(filePath=mojoFMResPreFilePath, clusterResult=clusterResult)

    colorDict = getRealColor(variable=variables_construct)

    mojoFMResRealFilePath = r'.\cluster\algos\agk\data\txtFile\mojoFMFiles' + '\\' + SoftwareName + '-' + GraphEmbeddingAlgorithm + '-' + ClusterAlgorithm + '-' + 'MojoFM-Real.txt'
    writeResultMojoFMReal(colorDict=colorDict, filePath=mojoFMResRealFilePath)

    jsonCluster = {}

    data = []
    for clusterResultIndex in range(len(clusterResult)):
        temp = {}
        temp["name"] = 'cluster' + str(clusterResultIndex)
        children = []
        for childIndex in range(len(clusterResult[clusterResultIndex])):
            temp1 = {}
            name = clusterResult[clusterResultIndex][childIndex]
            temp1["name"] = name
            temp1["value"] = 0.025
            temp1["color"] = colorDict[name]
            children.append(temp1)
        temp["children"] = children
        data.append(temp)
    jsonCluster["data"] = data
    outJsonFilePath = r'.\cluster\algos\agk\data\outJsonFiles' + '\\' + SoftwareName + '-' + GraphEmbeddingAlgorithm + '-' + ClusterAlgorithm + '-' + 'out.json'
    with open(outJsonFilePath, 'w', encoding='utf-8') as jsonFile:
        json_str = json.dumps(jsonCluster, indent=4)
        jsonFile.write(json_str)
        jsonFile.close()
    return jsonCluster

