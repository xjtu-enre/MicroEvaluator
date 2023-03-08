import numpy as np

from evaluator.microevaluator.evolvability.ioe_measure import readCommit
from evaluator.microevaluator.evolvability.ioe_measure import readCluster
from evaluator.microevaluator.modularity.chameleon import getCoChangeCluster


def get_spread_and_focus(cmt_path, service_path):
    # cmt_path = 'C:\\Users\\20465\\Desktop\\codes\\codes\\codes\\Django_Part\\Django_Part\\Separate\\evaluator\\data\\UploadData\\test\\train-ticket\\0.0.1\\cmt.csv'
    # service_path = 'C:\\Users\\20465\\Desktop\\codes\\codes\\codes\\Django_Part\\Django_Part\\Separate\\evaluator\\data\\UploadData\\test\\train-ticket\\0.0.1\\plan1\\sc.csv'
    # 创建coChangeGraph
    commit = readCommit(cmt_path)
    coChangeGraph, vertexes = getCoChangeGraph(commit)
    # print(coChangeGraph)
    # 提取coChangeCluster
    coChangeCluster = getCoChangeCluster(coChangeGraph)
    # print(coChangeCluster)
    # 为聚类结果去重，并且转换为服务名表示的形式
    coChangeCluster = deduplication(coChangeCluster, vertexes)
    # print(coChangeCluster)
    # 微服务与对应的类的集合
    [service2Class, class2serviceDict] = readCluster(service_path, 'fosci')
    # 计算focus和spread()
    focus, spread, services = competeSpreadAndFocus(coChangeCluster, service2Class)
    focusdic, spreaddic = get_focus_and_spread_dict(focus, spread, services)

    return focusdic, spreaddic, float(format(sum(focus) / len(services), '.4f')), float(
        format(sum(spread) / len(services), '.4f'))


def get_focus_and_spread_dict(focus, spread, services):
    focusdic = dict()
    spreaddic = dict()
    for index in range(0, len(services)):
        focusdic[services[index]] = focus[index]
        spreaddic[services[index]] = spread[index]

    return focusdic, spreaddic


def deduplication(coChangeCluster, vertexes):
    finalCoChangeCluster = []
    for index1 in range(0, len(coChangeCluster)):
        tempCLuster = []
        for index2 in range(0, len(coChangeCluster[index1])):
            serviceName = vertexes[coChangeCluster[index1][index2]]
            if serviceName not in tempCLuster:
                tempCLuster.append(serviceName)
        finalCoChangeCluster.append(tempCLuster)
    return finalCoChangeCluster


def getCoChangeGraph(commit):
    vertexes = []
    commitMatrix = [[0] * len(commit) for _ in range(len(commit))]
    # 获得共变图顶点集合
    for item in commit:
        vertexes.append(item)
    # 使用双重循环遍历顶点集合并将权值放入共变矩阵里面
    for index1 in range(0, len(vertexes)):
        for index2 in range(0, len(vertexes)):
            if vertexes[index2] in commit[vertexes[index1]]:
                commitMatrix[index1][index2] = commit[vertexes[index1]][vertexes[index2]]
            else:
                commitMatrix[index1][index2] = 0

    # print(commitMatrix)
    # print(vertexes)
    return np.array(commitMatrix), np.array(vertexes)


def competeSpreadAndFocus(coChangeCluster, service2Class):
    # coChangeCluster = [{'a', 'b'}, {'c'}, {'d', 'e', 'f'}]
    # service2Class = {'0': ['a'], '1': ['f'], '2': ['d'], '3': ['c', 'b', 'e']}
    serviceModularity = dict()
    focus = []
    spread = []
    for serviceID in service2Class:
        # if (serviceID == 'Document'):
        # print(service2Class[serviceID])
        # if (serviceID == 'Json2Shiviz'):
        #     print(service2Class[serviceID])
        tempSpread = 0
        tempFocus = 0
        for cluster in coChangeCluster:
            # tempCount记录集群和微服务之间的交集个数
            tempCount = 0
            # 设置一个flag，记录tempSpread的个数是否进行变化；若已经遍历过该微服务，tempSpread个数不进行变化，反之加1
            flag = False
            for item1 in service2Class[serviceID]:
                for item2 in cluster:
                    if item1 == item2:
                        if not flag:
                            flag = True
                            tempSpread = tempSpread + 1
                        tempCount = tempCount + 1
            tempFocus = tempFocus + (tempCount / len(service2Class[serviceID])) * (tempCount / len(cluster))
        focus.append(float(format(tempFocus, '.4f')))
        spread.append(float(format(tempSpread / len(coChangeCluster), '.4f')))
    # 对spread值进行归一化
    # spreadResult = spreadNormalized(spread)
    return focus, spread, list(service2Class.keys())


def spreadNormalized(tempSpread):
    temp = []
    min = np.min(tempSpread)
    max = np.max(tempSpread)

    for spread in tempSpread:
        # 如果spread为0或1代表质量很好;2-5之间归一化到0.5;大于5直接归一化到0
        if max - min == 0 and max < 2:
            temp.append(1)
        # spread越小越好
        temp.append((max - spread) / (max - min))

    return temp


if __name__ == '__main__':
    get_spread_and_focus()
