import csv
from evaluator.microevaluator.modularity import config

'''
load data from function atom files, calldep files, concerndep files.

generate global allAtoms,  classDepDict


interface:
    loadClassList()
    loadDepData(calldepFile, concerndepFile)
'''

#dep between class
class DepElement:
    def __init__(self, calldep, concerndep):
        self.calldep = calldep
        self.concerndep = concerndep

#load the class whose dep will be computed.
#output:
#classIDNameDict
#classNameIDDict
def loadClassList(filename):
    classIDNameDict = dict()
    indivDict = dict()  # dict[clustername] = [classid]
    with open(filename, "r", newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [contain, clustername, classname, classid] = each
            classid = int(classid)
            classIDNameDict[classid] = classname
            if clustername not in indivDict:
                indivDict[clustername] = list()
            indivDict[clustername].append(int(classid))

    # from dict to list
    indiv = list()
    for clusterId in indivDict:
        indiv.append(indivDict[clusterId])
    return classIDNameDict, indiv, indivDict

def readCSV(filename):
    listList = list()
    with open(filename, "r", newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            listList.append(each)
    return listList


def getDict(depList, classIDNameDict):
    # ClassName2IDDict = config.get_classnameid_dict()
    #print(ClassName2IDDict)
    classDepDict = dict()
    for each in depList:
        [class1, class2, dep] = each
        # 此处其实如果是不同的微服务中存在相同名字的类，那么其实每次都是取得第一次出现的类id(因为无法区分到底是哪个微服务内的)
        if class1 not in classIDNameDict.values() or class2 not in classIDNameDict.values():
            continue
        # classId1 = ClassName2IDDict[class1]
        # classId2 = ClassName2IDDict[class2]
        classId1 = get_classid(class1, classIDNameDict)
        classId2 = get_classid(class2, classIDNameDict)
        if classId1 not in classDepDict:
            classDepDict[classId1] = dict()
        if classId2 not in classDepDict[classId1]:
            classDepDict[classId1][classId2] = float(dep)
    return classDepDict

def get_classid(classname, classIDNameDict):
    for classid in classIDNameDict:
        if classIDNameDict[classid] == classname:
            return classid

#calldep = c1->c2 + c2->c1
def getCallDep(class1, class2, depDict):
    dep  = 0
    if class1 in depDict and class2 in depDict[class1]:
        dep += depDict[class1][class2]
    if class2 in depDict and class1 in depDict[class2]:
        dep += depDict[class2][class1]
    return dep

#concernDep = c1->c2   or   c2->c1
def getConcernDep(class1, class2, depDict):
    if class1 in depDict and class2 in depDict[class1]:
        return depDict[class1][class2]
    if class2 in depDict and class1 in depDict[class2]:
        return depDict[class2][class1]
    return 0


#generate all deps between all classes based on above loaded deps.
def genFinalDep(classIdList, calldepDict, concernDepDict):
    # print(len(classIdList))
    classDepDict = dict()  #dict[class1][class2] = DepElement(calldep, concerndep)
    for index1 in range(0, len(classIdList)):
        class1 = classIdList[index1]
        if class1 not in classDepDict:
            classDepDict[class1] = dict()
        for index2 in range(0, len(classIdList)):
            class2 = classIdList[index2]
            if class1 != class2:
                callvalue = getCallDep(class1, class2, calldepDict)
                concernValue = getConcernDep(class1, class2, concernDepDict)
                classDepDict[class1][class2] = DepElement(callvalue, concernValue)
    return classDepDict



#compute class-class dep for double - directed. c1->c2= c2->c1
#generate global allAtoms,  classDepDict
def loadDepData(calldepFile, concerndepFile, classIDNameDict):
    #load different dep
    calldepList = readCSV(calldepFile)
    concerndepList = readCSV(concerndepFile)
    calldepDict = getDict(calldepList, classIDNameDict)
    concernDepDict = getDict(concerndepList, classIDNameDict)

    #generate final deps between all classes based on above loaded deps.
    classIdList = list(classIDNameDict.keys())
    classDepDict = genFinalDep(classIdList, calldepDict, concernDepDict)
  
    return classDepDict



def test():
    #test
    import sys
    atomfileName = sys.argv[1]
    calldepFile = sys.argv[2]
    concerndepFile = sys.argv[3]
    #load and store atoms.
    [classIDNameDict, classNameIDDict, allAtoms] = readAtomFile(atomfileName)
    config.set_allatom_list(allAtoms)
    config.set_classidname_dict(classIDNameDict)
    config.set_classnameid_dict(classNameIDDict)

    #print("classIDNameDict", classIDNameDict)
    #print("classNameIDDict", classNameIDDict)
    #print("atoms:")
    #for atom in allAtoms:
    #    print(atom.atomId, atom.classIdSet)

    #load different dep
    calldepList = readCSV(calldepFile)
    concerndepList = readCSV(concerndepFile)
    calldepDict = getDict(calldepList, classNameIDDict)
    concernDepDict = getDict(concerndepList, classNameIDDict)
    #print("call:", calldepDict)
    #print("concern:", concernDepDict)

    #generate final deps between all classes based on above loaded deps.
    classIdList = list(classIDNameDict.keys())
    classDepDict = genFinalDep(classIdList, calldepDict, concernDepDict)
    #print("final:")
    #for each1 in classDepDict:
    #    for each2 in classDepDict[each1]:
    #        print(classDepDict[each1][each2].calldep,classDepDict[each1][each2].concerndep )

    #store the data into gloabal config variable.
    config.set_classfinaldep_dict(classDepDict)

    #print(config.GLOBAL_VAR_OBJECT.ALLATOM_List)
    #print(config.GLOBAL_VAR_OBJECT.CLASSNAMEIDDict)
    #print(config.GLOBAL_VAR_OBJECT.CLASSIDNAMEDict)
    #print(config.GLOBAL_VAR_OBJECT.CLASSFINALDEPDict)
