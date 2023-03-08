import csv
import os
#tranaction = ["s1->s2", "..."]

#read service design result
#[contain, clusterId, classname]
def readService(filename):
    servicelist = list()
    classnameToServiceDict = dict()
    with open(filename, "r", newline="") as fp:
        reader = csv.reader(fp,delimiter=",")
        for each in reader:
            [contain, serviceID, classname, classid] = each
            classnameToServiceDict[classname] = serviceID
            if serviceID not in servicelist:
                servicelist.append(serviceID)
    return classnameToServiceDict, len(servicelist), servicelist


#trace=[[c1,c2], [c2,c3]]
def readTrace(filename):
    res = list()
    with open(filename, "r", newline="") as fp:
        reader = csv.reader(fp,delimiter=",")
        preID = "-1"
        atrace = list()
        for each in reader:
            [traceID,order,structtype,method1,method2,m1_para,m2_para,class1,class2,m1_return,m2_return] = each
            if traceID == "traceID":
                continue
            if preID != traceID:
                if preID != "-1":
                    res.append(atrace)
                preID = traceID
                atrace = list()

            atrace.append([class1, class2])

        res.append(atrace)
    return res



def genTransaction(servicefilename, tracefilename):
    [class2serviceDict, service_number, servicelist] = readService(servicefilename)
    tracelist = readTrace(tracefilename)

    tran_list = list()
    for atrace in tracelist:
        atrans = set()
        for each in atrace:
            [c1, c2] = each
            s1 = class2serviceDict[c1]
            s2 = class2serviceDict[c2]
            if s1== s2:
                strstr = s1
            else:
                strstr = s1 + "->" + s2
            atrans.add(strstr)
        tran_list.append(list(atrans))
    return tran_list, service_number


def genTransaction_singleservice(servicefilename, tracefilename):
    [class2serviceDict, service_number, servicelist] = readService(servicefilename)
    tracelist = readTrace(tracefilename)

    tran_list = list()
    for atrace in tracelist:
        atrans = set()
        for each in atrace:
            [c1, c2] = each
            s1 = class2serviceDict[c1]
            s2 = class2serviceDict[c2]
            atrans.add(s1)
            atrans.add(s2)
            #print(c1,s1,c2,s2)
        tran_list.append(list(atrans))
    return tran_list, service_number, servicelist
