import sys
import csv
import re

'''
g_clusterID2Interf2APIDict #[clusterID][interface] = list[api id ...]
g_apiDict #[api id] = api object
'''

#api is operation
class APIObject:
    def __init__(self, clusterID, interface, apiName, itemSet):
        self.clusterID = clusterID
        self.interface = interface
        self.apiName = apiName
        self.itemSet = itemSet

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

def IsIgnored(item, g_ignore_items):
    if item in g_ignore_items:
        return True
    else:
        return False

#for each ele, split by hump
def SplitHump(oneList):
    resList = list()
    for name in oneList:
        upperIndexList = list()
        upperIndexList.append(0) #first index
        for index in range(0, len(name)):
            if name[index].isupper():
                upperIndexList.append(index)
        upperIndexList.append(index + 1) #last index + 1

        for i in range(0, len(upperIndexList) - 1):
            index_s = upperIndexList[i]
            index_e = upperIndexList[i + 1]
            strstr = name[index_s: index_e]
            resList.append(strstr)
    return resList

#split(., tuofeng) each name to items, and ignore the non-domain item
def GetItems(nameSet, g_ignore_items):
    itemList = list()
    for name in nameSet:
        #split, for xwiki, the filter words shoud delete the first three pacakageprefix
        tmp = name.split('.')
        if len(tmp) > 3:
            name =  tmp[len(tmp) - 3] + "." + tmp[len(tmp) - 2]+ "." + tmp[len(tmp) - 1]
        ############
        tmpList = re.split( r'[._]', name)
        tmpList = SplitHump(tmpList)
        tmpList = [each.lower() for each in tmpList]
        itemList.extend(tmpList)
    newItemList = list()
    for item in itemList:
        if IsIgnored(item, g_ignore_items) == False and item != '':
            newItemList.append(item)
    #print ('before=', set(nameSet))
    #print ('after =', set(newItemList))
    return set(newItemList)

def ReadAPIFile(serviceFileName, fileName,fileType, g_ignore_items):
    apiID = 0
    clusterID2Interf2ApiDict = dict()
    apiDict = dict()

    # read all clusternames
    all_clusters = []
    with open(serviceFileName, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [contain, clustername, classname, classid] = each
            all_clusters.append(clustername)

    with open(fileName,'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            if fileType == 'fome':
                [clusterID, interfName, apiName, parameterstr, returnstr] = each
            else:
                [clusterID, apiName, parameterstr, returnstr] = each
            if each[0] == 'clusterID':
                continue
            #clusterID = int(clusterID)
            parameterSet = Trans2Set(parameterstr)
            returnSet = Trans2Set(returnstr)
            interface = GetInterf(apiName)
            if clusterID not in clusterID2Interf2ApiDict:
                clusterID2Interf2ApiDict[clusterID] = dict()
            if interface not in clusterID2Interf2ApiDict[clusterID]:
                clusterID2Interf2ApiDict[clusterID][interface] = list()
            nameSet = parameterSet | returnSet
            nameSet.add(apiName)
            itemSet = GetItems(nameSet, g_ignore_items)
            oneObejct = APIObject(clusterID, interface, apiName, itemSet)
            #print nameSet
            #print oneObejct.itemSet
            apiDict[apiID] = oneObejct
            clusterID2Interf2ApiDict[clusterID][interface].append(apiID)
            apiID += 1

    # 不存在对外接口的微服务api为0
    for cluster in all_clusters:
        if cluster not in clusterID2Interf2ApiDict:
            clusterID2Interf2ApiDict[cluster] = 0

    return clusterID2Interf2ApiDict, apiDict

#domain-level edge weight
def GetEdge(apiID1, apiID2, g_apiDict):
    itemSet1 = g_apiDict[apiID1].itemSet
    itemSet2 = g_apiDict[apiID2].itemSet
    # print (g_apiDict[apiID1].interface, g_apiDict[apiID1].apiName, itemSet1)
    # print (g_apiDict[apiID2].interface, g_apiDict[apiID2].apiName, itemSet2)
    '''
    if len(itemSet1) == 0 and len(itemSet2) == 0:  #not have domain items, then return 1
        edge_wei = 1
        edge_unwei = 1
    '''
    interSet = itemSet1 & itemSet2
    unionSet = itemSet1 | itemSet2
    #print('itemSet1', itemSet1)
    #print('itemSet2', itemSet2)
    #print('unionset', unionSet)
    if len(unionSet) == 0:
        return -1, -1
    edge_wei = len(interSet) / float(len(unionSet))
    if len(interSet) != 0:
        edge_unwei = 1.0
    else:
        edge_unwei = 0.0
    return edge_wei, edge_unwei

#get api list for a cluster
##g_clusterID2Interf2APIDict[clusterID][interface] = [api id ....]
def getAllAPIForCluster(clusterID, g_clusterID2Interf2APIDict):
    apiIDList = list()
    for interface in g_clusterID2Interf2APIDict[clusterID]:
        apis = g_clusterID2Interf2APIDict[clusterID][interface]
        apiIDList.extend(apis)
    return apiIDList


#compute the interface's dom_cohesion
def Metric_dom_cohesion(clusterID, g_clusterID2Interf2APIDict, g_apiDict):
    apiIDList = getAllAPIForCluster(clusterID, g_clusterID2Interf2APIDict)
    if len(apiIDList) == 1:
        dom_cohesion_wei = 1.0
    else:
        from itertools import combinations
        apiIDPairList = list(combinations(apiIDList, 2))
        sim_wei_list = list()
        for apiIDpair in apiIDPairList:
            [edge_wei, edge_unwei] = GetEdge(apiIDpair[0], apiIDpair[1], g_apiDict)
            if edge_wei != -1:
                sim_wei_list.append(edge_wei)
        dom_cohesion_wei = sum(sim_wei_list) / float(len(sim_wei_list))
    return dom_cohesion_wei

def interface_dom_cohesion_method(serviceFileName, apiFileName, fileType):
    #apiFileName = sys.argv[1]
    #fileType = sys.argv[2]

    g_ignore_items = ['jpetstore', 'jforum', 'xwiki', 'roller', 'agilefant', 'blog', 'raysmond',\
                      'b3log', 'solo', 'fi', 'hut', 'soberit', 'agilefant', 'servlets', 'javax',\
                      'java', 'net', 'org', 'common', 'lang', 'apache', 'roller', 'weblogger', 'int',\
                      'math', 'string', 'int', 'void', 'date', 'object', 'list',\
                      'get', 'set', 'decimal', 'boolean', 'action', 'service', 'bean',\
                      'service', 'repository', 'controller', 'data', 'dto', 'common', 'id', 'processor',\
                      'solo', 'service', 'repository', 'process', 'controller', 'data', 'date', 'dto',\
                      'common', 'id', 'processor', 'impl', 'cache','mgmt', 'query', 'console',\
                      'service', 'hsqldb', 'type', 'dao', 'acces', 'default', 'generic', 'common', 'action',\
                      'repository', 'process', 'control', 'controller', 'data', 'date', 'dto', 'common', 'id', \
                      'processor', 'impl', 'cache','mgmt', 'query', 'console', 'comparator',
                      'exception', 'provider', 'impl', 'bean', 'edit', 'action', 'interceptor', 'factory', \
                      'common', 'data', 'servlet', 'view','base','management', 'request', 'cache', 'manage',\
                      'manager', 'manag', 'pager', 'pag', 'model', 'service', 'wrapper','wrapp', 'weblog', \
                      'comparator', 'accessor', 'task', 'jpa', 'abstract', 'action', 'container', 'interceptor', 'business',\
                      'impl', 'version_data', 'load', 'filter', 'hierarchy', 'dao', 'hibernate', 'entry', 'generator', \
                      'agilefant', 'to', 'type', 'data', 'node', 'metric', 'handle', 'manager', 'manage',\
                      'default', 'service', 'config', 'filter', 'filt', 'listen', 'render', 'abstract', 'typ', 'string', \
                      'request',  'resource', 'response', 'object', 'factory', 'access', 'model', 'action', 'abstract', \
                      'customiz', 'generator', 'load',  'build', 'listen', 'descriptor', 'script', 'repository', 'action', \
                      'cache', 'type',  'resolve', 'convert', 'and', 'provid', 'of', 'in', 'list', 'from', 'impl', 'check', \
                      'serializer', 'serialize', 'xwiki', 'wiki', 'context','reference', 'translation', 'configuration',\
                      'annotation', 'bridge']

    [g_clusterID2Interf2APIDict, g_apiDict] = ReadAPIFile(serviceFileName, apiFileName, fileType, g_ignore_items)
    dom_cohesion_wei_list = list()
    domperservicedict = dict()
    servicenum_whohasinf = 0
    if len(g_clusterID2Interf2APIDict) == 0:
        avg_dom_cohesion_wei = 1.0
        interface_number = 0
    else:
        interface_number = 0
        for clusterID in g_clusterID2Interf2APIDict:
            if g_clusterID2Interf2APIDict[clusterID] == 0:
                dom_cohesion_wei_list.append(1)
                domperservicedict[clusterID] = 1
                interface_number += 0
            else:
                dom_cohesion_wei = Metric_dom_cohesion(clusterID, g_clusterID2Interf2APIDict, g_apiDict)
                dom_cohesion_wei_list.append(dom_cohesion_wei)
                domperservicedict[clusterID] = ("%.4f" % dom_cohesion_wei)
                interface_number += len(g_clusterID2Interf2APIDict[clusterID])
            servicenum_whohasinf = servicenum_whohasinf + 1
        avg_dom_cohesion_wei = ("%.4f" % (sum(dom_cohesion_wei_list) / float(len(dom_cohesion_wei_list))))
    return avg_dom_cohesion_wei, "%.4f" % (interface_number/float(servicenum_whohasinf)), domperservicedict, servicenum_whohasinf
