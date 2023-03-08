import sys
import csv

#g_clusterID2Interf2APIDict #[clusterID][interface] = list[api id ...]
#g_apiDict #[api id] = api object

#api is operation
class APIObject:
    def __init__(self, clusterID, interface, apiName, parameterSet, returnSet):
        self.clusterID = clusterID
        self.interface = interface
        self.apiName = apiName
        self.parameterSet = parameterSet
        self.returnSet = returnSet

def Trans2Set(strstr):
    if strstr == '':
        resList = ['void']
    else:
        resList = strstr.split(',')
    return set(resList)

def GetInterf(api):
    #interface name
    apiList = api.split('.')
    del apiList[len(apiList) - 1]
    interface = '.'.join(apiList)
    return interface


def ReadAPIFile(serviceFileName, fileName, fileType):
    apiID = 0
    clusterID2Interf2ApiDict = dict()
    apiDict = dict()

    # read all clusternames
    all_clusters = []
    with open(serviceFileName, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [contain, clustername, classname, classid] = each
            if clustername not in all_clusters:
                all_clusters.append(clustername)

    with open(fileName, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            if fileType == 'fome':
                [clusterID, interfName, apiName, parameterstr, returnstr] = each
            else:
                [clusterID, apiName, parameterstr, returnstr] = each
            if each[0] == 'clusterID':
                continue
            if clusterID not in all_clusters:
                continue
            parameterSet = Trans2Set(parameterstr)
            returnSet = Trans2Set(returnstr)
            interface = GetInterf(apiName)
            if clusterID not in clusterID2Interf2ApiDict:
                clusterID2Interf2ApiDict[clusterID] = dict()
            if interface not in clusterID2Interf2ApiDict[clusterID]:
                clusterID2Interf2ApiDict[clusterID][interface] = list()
            oneObejct = APIObject(clusterID, interface, apiName, parameterSet, returnSet)
            apiDict[apiID] = oneObejct
            clusterID2Interf2ApiDict[clusterID][interface].append(apiID)
            apiID += 1

    # 不存在对外接口的微服务api为0
    for cluster in all_clusters:
        if cluster not in clusterID2Interf2ApiDict:
            clusterID2Interf2ApiDict[cluster] = 0

    return clusterID2Interf2ApiDict, apiDict


def GetIntersect(apiID1, apiID2, g_apiDict):
    para_interset = g_apiDict[apiID1].parameterSet & g_apiDict[apiID2].parameterSet
    return_interset = g_apiDict[apiID1].returnSet & g_apiDict[apiID2].returnSet
    return para_interset, return_interset


def GetUnionset(apiID1, apiID2, g_apiDict):
    para_unionset = g_apiDict[apiID1].parameterSet | g_apiDict[apiID2].parameterSet
    return_unionset = g_apiDict[apiID1].returnSet | g_apiDict[apiID2].returnSet
    return para_unionset, return_unionset


#compute the edge between two apis
#if have common para/return type, then have an edge between the two operations/apis
def GetEdge_half(interSet, unionSet):
    edge_unwei = 0
    edge_wei = 0
    if len(unionSet) == 0:
        return -1, -1
    if len(interSet) != 0:
        edge_unwei = 1
        edge_wei = len(interSet) / float(len(unionSet))
    #print edge_unwei, edge_wei
    return edge_unwei, edge_wei

#get api list for a cluster
##g_clusterID2Interf2APIDict[clusterID][interface] = [api id ....]
def getAllAPIForCluster(clusterID, g_clusterID2Interf2APIDict):
    apiIDList = list()
    for interface in g_clusterID2Interf2APIDict[clusterID]:
        # if int(interface) == 0:
        #     apiIDList.append(-1)
        #     continue
        apis = g_clusterID2Interf2APIDict[clusterID][interface]
        apiIDList.extend(apis)
    return apiIDList



#measure the meg-level 's interface cohesion'
def Metric_msg_cohesion(clusterID, g_clusterID2Interf2APIDict, g_apiDict):
    apiIDList = getAllAPIForCluster(clusterID, g_clusterID2Interf2APIDict)
    if len(apiIDList) == 1:
        cohesion_wei = 1
    else:
        from itertools import combinations
        apiIDPairList = list(combinations(apiIDList, 2))
        fenmu = len(apiIDPairList)  #perfect graph's edge number
        apiSimList = list()
        for apiPair in apiIDPairList:
            [para_interset, return_interset] = GetIntersect(apiPair[0], apiPair[1], g_apiDict)
            [para_unionset, return_unionset] = GetUnionset(apiPair[0], apiPair[1], g_apiDict)
            [para_unweight, para_weight] = GetEdge_half(para_interset, para_unionset)
            [return_unweight, return_weight] = GetEdge_half(return_interset, return_unionset)
            if para_weight != -1 and return_weight != -1:
                sim = (para_weight + return_weight ) / float(2.0)
                apiSimList.append(sim)
            elif para_weight == -1 and return_weight != -1:
                sim = return_weight
                apiSimList.append(sim)
            elif para_weight != -1 and return_weight == -1:
                sim = para_weight
                apiSimList.append(sim)
        # print(apiSimList)
        cohesion_wei = sum(apiSimList) / float(len(apiSimList))
    return cohesion_wei



def interface_msg_cohesion_method(serviceFileName, apiFileName, fileType):
    [g_clusterID2Interf2APIDict, g_apiDict] = ReadAPIFile(serviceFileName, apiFileName, fileType)
    msg_cohesion_wei_list = list()
    msg_cohesion_per_service = dict()
    infnum_per_service = dict()
    interface_number = 0
    servicenum_whohasinf = 0
    if len(g_clusterID2Interf2APIDict) == 0:
        tmp =['avg_msg_cohesion', str(1), 'interface_numb', str(0), 'clusterHasinf', str(0)]
        msg_avg_wei = 1
        interface_number = 0
    else:
        for clusterID in g_clusterID2Interf2APIDict:
            if g_clusterID2Interf2APIDict[clusterID] == 0:
                msg_cohesion_per_service[clusterID] = 1
                msg_cohesion_wei_list.append(1)
                infnum_per_service[clusterID] = 0
                interface_number += 0
            else:
                msg_cohesion_wei = Metric_msg_cohesion(clusterID, g_clusterID2Interf2APIDict, g_apiDict)
                msg_cohesion_wei_list.append(msg_cohesion_wei)
                msg_cohesion_per_service[clusterID] = ("%.4f" % msg_cohesion_wei)
                infnum_per_service[clusterID] = len(g_clusterID2Interf2APIDict[clusterID])
                interface_number += len(g_clusterID2Interf2APIDict[clusterID])
            servicenum_whohasinf += 1
        msg_avg_wei = ("%.4f" % (sum(msg_cohesion_wei_list) / float(len(msg_cohesion_wei_list))))

    return msg_avg_wei, ("%.4f" % (interface_number/float(servicenum_whohasinf))), msg_cohesion_per_service, infnum_per_service



def getservicelist(serviceFileName):
    scIDList = list()
    with open(serviceFileName, "r", newline="") as fp:
        reader = csv.reader(fp, delimiter=",")
        for each in reader:
            [contain, serviceID, classname] = each
            if serviceID not in scIDList:
                scIDList.append(serviceID)
    return scIDList
