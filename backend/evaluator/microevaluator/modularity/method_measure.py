import csv

# dep between method
class MethodDepElement:
    def __init__(self, method1, class1, method2, class2, dep):
        self.method1 = method1
        self.class1 = class1
        self.method2 = method2
        self.class2 = class2
        self.dep = dep

def measure_method(methoddepFile, classFile, serviceFileName):
    serviceDict, services_to_num = readCSV(classFile, serviceFileName)
    dep_elements = get_method_dep(methoddepFile)
    m_ch, in_count = compete_mch(serviceDict, services_to_num, dep_elements)
    m_cp, out_count = compete_mcp(serviceDict, services_to_num, dep_elements)
    density = compete_density(in_count, out_count)
    return m_ch, m_cp, density

def readCSV(classFile, serviceFileName):
    class2service = dict()
    classid2name = dict()
    serviceDict = dict()  # dict[clustername] = [classid]
    with open(serviceFileName, "r", newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [contain, clustername, classname, classid] = each
            class2service[classid] = clustername
            classid2name[classid] = classname
            if clustername not in serviceDict:
                serviceDict[clustername] = list()
            serviceDict[clustername].append(classname)

    services_to_num = dict()
    with open(classFile, "r", newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [classname, methodnum] = each
            for service in serviceDict:
                if classname in serviceDict[service]:
                    if service not in services_to_num:
                        services_to_num[service] = 0
                    services_to_num[service] = services_to_num[service] + int(methodnum)
                    continue

    return serviceDict, services_to_num


def get_method_dep(methoddepFile):
    dep_elements = list()
    with open(methoddepFile, "r", newline="") as fp:
        reader = csv.reader(fp)
        # each:[method1, class1, method2, class2, dep]
        for each in reader:
            [method1, class1, method2, class2, dep] = each
            dep_elements.append(MethodDepElement(method1, class1, method2, class2, int(dep)))

    return dep_elements


# serviceDict:{sc1:[calss1,class2,..], sc2:[calss1,class2,..],...} services_to_num:{sc1:methodnum,...}  dep_elements:[MethodDepElement1, MethodDepElement2,...]
def compete_mch(serviceDict, services_to_num, dep_elements):
    mch = 0
    in_count = 0
    for item in services_to_num:
        count = 0
        for element in dep_elements:
            if element.class1 in serviceDict[item] and element.class2 in serviceDict[item] and element.dep != 0:
                count = count + 1
        mch = mch + count / (services_to_num[item] * services_to_num[item])
        in_count = in_count + count
    return mch / len(services_to_num), in_count

def compete_mcp(serviceDict, services_to_num, dep_elements):
    mcp = 0
    out_count = 0
    testcount = 0
    for index1 in range(0, len(serviceDict)):
        classes1 = serviceDict[list(serviceDict.keys())[index1]]
        for index2 in range(index1 + 1, len(serviceDict)):
            testcount = testcount + 1
            classes2 = serviceDict[list(serviceDict.keys())[index2]]
            count = 0
            for element in dep_elements:
                if ((element.class1 in classes1 and element.class2 in classes2) or (element.class1 in classes2 and element.class2 in classes1)) and element.dep != 0:
                    count = count + 1
            mcp += count / (services_to_num[list(serviceDict.keys())[index1]] * services_to_num[list(serviceDict.keys())[index2]])
            out_count = out_count + count
    return 2 * mcp / (len(services_to_num) * (len(services_to_num) - 1)), out_count

def compete_density(in_count, out_count):
    return in_count / (in_count + out_count)
