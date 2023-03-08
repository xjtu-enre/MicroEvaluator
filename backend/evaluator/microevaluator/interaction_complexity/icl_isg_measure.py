import csv
from evaluator.microevaluator.interaction_complexity.transaction import readTrace,readService


#traceDict[traceId][(opr1,opr2)]=times
def readTraceAtOperationLevel(filename):
    traceDict = dict()
    traceIDList = list()
    oprpairList = list()
    with open(filename, "r", newline="") as fp:
        reader = csv.reader(fp,delimiter=",")
        preID = "-1"
        atrace = list()
        for each in reader:
            [traceID,order,structtype,method1,method2,m1_para,m2_para,class1,class2,m1_return,m2_return] = each
            if traceID == "traceID":
                continue
            if traceID not in traceDict:
                traceDict[traceID] = dict()
            if (method1, method2) not in traceDict[traceID]:
                traceDict[traceID][(method1,method2)] = 0
            traceDict[traceID][(method1,method2)] += 1

            if traceID not in traceIDList:
                traceIDList.append(traceID)
            if (method1, method2) not in oprpairList:
                oprpairList.append((method1, method2) )

    return traceDict, traceIDList, oprpairList



def readTraceAtServiceLevel(filename):
    traceDict = dict()
    traceIDList = list()
    servicepairList = list()
    with open(filename, "r", newline="") as fp:
        reader = csv.reader(fp, delimiter=",")
        preID = "-1"
        atrace = list()
        for each in reader:
            [traceID,  service1, service2, opr] = each
            if traceID == "traceID" or traceID == 'TraceID':
                continue
            if traceID not in traceDict:
                traceDict[traceID] = dict()
            if (service1, service2) not in traceDict[traceID]:
                traceDict[traceID][(service1, service2)] = 0
            traceDict[traceID][(service1, service2)] += 1

            if traceID not in traceIDList:
                traceIDList.append(traceID)
            if (service1, service2) not in servicepairList:
                servicepairList.append((service1, service2))

    return traceDict, traceIDList, servicepairList


#DSM=
#" "     (opr1,opr2)   (opr3,opr4)
#trace1,    X,             X
#trace2,    X ,            X
def genbehaviorDSM(traceDict, traceIDList, oprpairList):
    DSM = list()

    firstrow = [" "]
    firstrow.extend(oprpairList)
    DSM.append(firstrow)

    for i in range(0, len(traceIDList)) :
        tmp =[i]
        tmp.extend([" "]*len(oprpairList))
        DSM.append(tmp)


    for i in range(0, len(traceIDList)):
        for j in range(0, len(oprpairList)):
            traceID = traceIDList[i]
            oprpair = oprpairList[j]
            if traceID in traceDict and oprpair in traceDict[traceID]:
                times =  traceDict[traceID][oprpair]
                DSM[i+1][j+1] = times
    ''''
    print("operation DSM:")
    for row in DSM:
        print (row)
    '''
    return (DSM)


#atrace=[ [s1,s2], [s2,s2], [...] ]
def beforecalculate(tracelist, classnameToServiceDict):
    res = list()
    for onetrace in tracelist:
        tmp = list()
        for each in onetrace:
            [c1, c2] = each
            s1 = classnameToServiceDict[c1]
            s2 = classnameToServiceDict[c2]
            tmp.append([c1,c2])
        res.append(tmp)
    return res

'''
isg is the number of different services for processing one trace
'''
def calculateISG(alist, traceIDList):
    if len(alist) != len(traceIDList):
        print('ERROR!', len(alist), len(traceIDList))

    isg_dict = dict()
    for index in range(0, len(alist)):
        traceID = traceIDList[index]
        eachtrace = alist[index]
        serviceset = set()
        for each in eachtrace:
            serviceset.add(each[0])
            serviceset.add(each[1])
        isg_dict[traceID] = len(serviceset)
    valuelist = list(isg_dict.values())
    ISG = sum(valuelist) / float(len(valuelist))
    return ISG, isg_dict


'''
icl is the inter-service call number for proessing each trace'''
def calculateICL(alist, traceIDList):
    if len(alist) != len(traceIDList):
        print('ERROR!', len(alist), len(traceIDList))

    icl_dict = dict()
    for index in range(0, len(alist)):
        traceID = traceIDList[index]
        eachtrace = alist[index]
        cross_service_call = 0
        for each in eachtrace:
            if each[0] != each[1]: #cross service call
                cross_service_call += 1
        icl_dict[traceID] = cross_service_call
    valuelist = list(icl_dict.values())
    ICL = sum(valuelist) / float(len(valuelist))
    return ICL, icl_dict


'''
calculateICL_ISG api
'''


def readServiceLevelTrace(tracefilename):
    tracelist = list()
    with open(tracefilename, "r", newline='') as fp:
        reader = csv.reader(fp, delimiter=',')
        alist = list()
        pretraceID = "-1"
        for each in reader:
            if each[0] == 'TraceID':
                continue
            [traceID, callerservice, calleeservice, operation] = each
            if traceID == 'TraceID' or traceID == 'traceID':
                continue
            if traceID != pretraceID: #new trace start
                if pretraceID != "-1":
                    tracelist.append(alist)
                alist  = list()
                pretraceID = traceID
                alist.append([callerservice, calleeservice])
            else:
                alist.append([callerservice, calleeservice])
        tracelist.append(alist)
    return tracelist



'''
isg and icl for each trace
'''
def calculateICL_ISG(servicefilename, tracefilename):
    if "Train-Ticket" not in tracefilename:
        [classnameToServiceDict, serviceLen, servicelist] = readService(servicefilename)
        # trace=[[c1,c2], [c2,c3]]
        tracelist = readTrace(tracefilename)
        [traceDict, traceIDList, oprpairList] = readTraceAtOperationLevel(tracefilename)
        behaviorDSM = genbehaviorDSM(traceDict, traceIDList, oprpairList)
        # atrace=[ [s1,s2], [s2,s2], [...] ]
        alist = beforecalculate(tracelist, classnameToServiceDict)
    else:
        alist = readServiceLevelTrace(tracefilename)
        [traceDict, traceIDList, servicepairList] = readTraceAtServiceLevel(tracefilename)
        behaviorDSM = genbehaviorDSM(traceDict, traceIDList, servicepairList)
    [ISG, isg_dict] = calculateISG(alist, traceIDList)
    [ICL, icl_dict] = calculateICL(alist, traceIDList)
    return ISG, ICL, isg_dict, icl_dict, behaviorDSM,traceIDList
