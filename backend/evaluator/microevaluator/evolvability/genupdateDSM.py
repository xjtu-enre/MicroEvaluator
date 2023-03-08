import csv

'''
commitfile each line [functionID, file, count]
featureDict[featureID][class]  = count
'''

def read_grouped_commits(commitfile):
    featureDict = dict()
    with open(commitfile, "r") as fp:
        reader = csv.reader(fp, delimiter=",")
        for each in reader:
            [featureID, file, count] = each
            if featureID not in featureDict:
                featureDict[featureID] = dict()
            featureDict[featureID][file]  = count
    return featureDict

'''
featureID file1 file2 ...
id1       count  count 
id2       x      cont
'''


def generate_updateDSM(featureDict):
    featureIDList = list()
    fileset = set()
    updationDSM = list()
    for featureID in featureDict:
        featureIDList.append(featureID)
        for file in featureDict[featureID]:
            fileset.add(file)
    fileList = list(fileset)

    firstrow = ['featureID'].extend(fileList)
    updationDSM.append(firstrow)
    for i in range(0, len(featureIDList)):
        featureID = featureIDList[i]
        row = [featureID]
        for j in range(0, len(fileList)):
            file = fileList[j]
            if featureID in featureDict and file in featureDict[featureID]:
                value = featureDict[featureID][file]
            else:
                value = ' '
            row.append(value)
        updationDSM.append(row)
    return updationDSM


#read service design result
#[contain, clusterId, classname]
def readService(filename):
    servicelist = list()
    classnameToServiceDict = dict()
    with open(filename, "r", newline="") as fp:
        reader = csv.reader(fp,delimiter=",")
        for each in reader:
            [contain, serviceID, classname] = each
            classnameToServiceDict[classname] = serviceID
            if serviceID not in servicelist:
                servicelist.append(serviceID)
    return classnameToServiceDict, len(servicelist)


'''
inter-service evloution: the service count per feature
ise_feature_list corresponds to ise_list
ise_list[i] is the ise value of feature from ise_feature_list[i]
'''

def calculate_ISE(classname2serviceDict, featureDict):
    ise_list = list()
    for featureID in featureDict:
        serviceset = set()
        for classname in featureDict[featureDict]:
            serviceset.add(classname2serviceDict[classname])
        ise_list.append(len(serviceset))
    ISE = sum(ise_list)/float(len(ise_list))
    ise_feature_list = list(featureDict.keys())
    return ISE, ise_list,ise_feature_list



'''
iis_list cooresonds to iis_interface_list
iis_list[i] is the iis value of the interface from iis_interface_list[i]
'''


def calculate_IIS(featureDict, interfaceList):

    interface_modifiedby_feature_dict = dict()  #[interface][featureID]=count
    for featureID in featureDict:
        for classname in featureDict[featureID]:
            if classname in interfaceList:
                if classname not in interface_modifiedby_feature_dict:
                    interface_modifiedby_feature_dict[classname] = dict()
                    interface_modifiedby_feature_dict[classname][featureID] = featureDict[featureID][classname]

    iis_list = list()
    iis_interface_list = list()
    for interfacename in interface_modifiedby_feature_dict:
        iis_interface_list.append(interfacename)
        tmplist = list()
        for featureID in interface_modifiedby_feature_dict[interfacename]:
            tmplist.append(interface_modifiedby_feature_dict[interfacename][featureID])
        iis_list.append( sum(tmplist) / float(len(tmplist)))

    IIS = sum(iis_list) / float(len(iis_list))
    return IIS, iis_list, iis_interface_list











