import sys
import csv
from evaluator.microevaluator.modularity import metric, loaddata, config


def prepare(clusterfilename, calldepFile, concerndepFile):
    # 根据sc.csv获取每个微服务对应的classid集合以及classIDNameDict
    [classIDNameDict, indiv, indivDict] = loaddata.loadClassList(clusterfilename)
    # config.set_classidname_dict(classIDNameDict)

    classDepDict = loaddata.loadDepData(calldepFile, concerndepFile, classIDNameDict)
    config.set_classfinaldep_dict(classDepDict)
    print("load data end...")

    return indiv, indivDict


def writeCSV(alist, filename):
    with open(filename, 'w', newline="") as fp:
        writer = csv.writer(fp)
        writer.writerows(alist)


def readClusterList(filename):
    fileList = list()
    with open(filename, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            clusterfilename = each[0]
            fileList.append(clusterfilename)
    return fileList


# reader clusterfile[contain, clusterid, classname], return indiv=[[classid1, classid2], []]
def getIndiv(clusterfilename):
    # className2IDDict = config.get_classnameid_dict()
    # print(len(className2IDDict))
    # print(len(config.get_classidname_dict()))
    indivDict = dict()  # dict[clusterID] = [classID]
    with open(clusterfilename, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [contain, clusterId, className, classId] = each
            # if className not in className2IDDict:
            #     continue
            # classId = className2IDDict[className]
            #clusterId = int(clusterId)
            if clusterId not in indivDict:
                indivDict[clusterId] = list()
            indivDict[clusterId].append(int(classId))

    # from dict to list
    indiv = list()
    for clusterId in indivDict:
        indiv.append(indivDict[clusterId])
    return indiv, indivDict


'''
api 
'''
def modularity_measure_method(calldepFile, concerndepFile, clusterfilename):
    print(clusterfilename)
    # 根据sc.apv和structuredep.csv、concerndep.csv获取到所有class的依赖集合
    fitness_method_list = config.GLOBAL_VAR_OBJECT.FITNESS_METHOD_LIST
    [indiv, indivDict] = prepare(clusterfilename, calldepFile, concerndepFile)

    # transform clusterfile ontent into indiv = [[id1, id2], [id4, id6], ...]
    # print('clusterfilename', clusterfilename)
    # indiv, indivDict = getIndiv(clusterfilename)
    # print('indiv', indiv)
    indivList = [indiv]
    # compute the metrics of all candidates in indivList
    metric.computeFitnessThread(indivList, fitness_method_list)

    # compute metrics for each indiv
    indiv = indivList[0]
    [call_coh, call_coup, con_coh, con_coup, call_coh_detail,call_coup_detail,con_coh_detail,con_coup_detail] = metric.get_four_metrics(indiv)
    #print("final call_coh, call_coup, concept_coh, concept_coup:", call_coh, call_coup, con_coh, con_coup)
    #print("call_coh_detail:", call_coh_detail)
    #print("call_coup_detail:", call_coup_detail)
    #print("con_coh_detail:", con_coh_detail)
    #print("con_coup_detail:", con_coup_detail)
    SMQ = call_coh - call_coup
    CMQ = con_coh - con_coup
    # print(call_coup_detail)
    # print(con_coup_detail)
    return SMQ, CMQ, call_coh_detail, call_coup_detail, con_coh_detail, con_coup_detail, indivDict.keys()




'''
test entry
'''

if __name__ == "__main__":
    classfileName = sys.argv[1]  # coverage releted
    calldepFile = sys.argv[2]  # coverage releted
    concerndepFile = sys.argv[3]
    fileListFile = sys.argv[4]  # contains clusters whose metric will be computed
    outmeasureFile = sys.argv[5]
    fitness_method_list = config.GLOBAL_VAR_OBJECT.FITNESS_METHOD_LIST
    prepare(classfileName, calldepFile, concerndepFile)

    # read all cluster files, putput indivList
    clusterFileList = readClusterList(fileListFile)
    indivList = list()  # this is consistent with clusterFileList
    for clusterfilename in clusterFileList:
        # indiv = [[id1, id2], [id4, id6], ...]
        indiv = getIndiv(clusterfilename)
        indivList.append(indiv)

    # compute the metrics of all candidates in indivList
    metric.computeFitnessThread(indivList, fitness_method_list)

    # compute metrics for each indiv
    measureList = list()
    for index in range(0, len(indivList)):
        print(clusterFileList[index])
        indiv = indivList[index]
        clusterfilename = clusterFileList[index]
        [call_coh, call_coup, con_coh, con_coup, call_coh_detail,call_coup_detail,con_coh_detail,con_coup_detail] = metric.get_four_metrics(indiv)
        tmp = [clusterfilename, call_coh, call_coup, con_coh, con_coup]
        measureList.append(tmp)

    # write measures into file
    writeCSV(measureList, outmeasureFile)
