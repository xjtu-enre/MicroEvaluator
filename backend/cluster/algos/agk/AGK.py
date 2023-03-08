import numpy as np
import math
from sklearn.cluster import KMeans


def caculateRange(data):
    rangei = []
    maxi = []
    mini = []
    for i in range(len(data[0])):
        max = np.max(data[:, i])
        min = np.min(data[:, i])
        rangei.append(max - min)
        maxi.append(max)
        mini.append(min)
    return rangei, maxi, mini


def FindTopK(center, k):
    knum = k
    while k > 0:
        k -= 1
        for centerNum in range(len(center) - 1):
            if center[centerNum][2] > center[centerNum+1][2]:
                tempNum = center[centerNum]
                center[centerNum] = center[centerNum+1]
                center[centerNum+1] = tempNum
    topK = center[len(center)-knum:len(center)]
    return topK


def AGK(dataInAlg, clusterNum):
    # calculate xsi
    DJ = []
    for i in range(len(dataInAlg[0])):
        DJ.append(np.std(dataInAlg[:, i]) / np.mean(dataInAlg[:, i]))
    DS = 1 / (1 + 1 / len(DJ) * (sum(DJ)))

    m = DS * (len(dataInAlg) ** (1 / len(dataInAlg[0])))
    xsi = int(np.ceil(m))

    rangei, maxi, mini = caculateRange(dataInAlg)

    K = clusterNum
    a = 1

    if K * 9 > math.sqrt(len(dataInAlg) / 2):
        GridNum = math.sqrt(len(dataInAlg) / 2)
    else:
        GridNum = K * 9

    # GridNum = xsi
    R = GridNum / (K + 1) * a
    GridNum = int(GridNum)
    print("GridNum", GridNum)
    # print("R", R)

    stepsi = []

    for i in range(len(rangei)):
        stepsi.append(rangei[i] / GridNum)

    Gridij = [[0] * len(dataInAlg[0])] * len(dataInAlg)
    Gridij = np.array(Gridij)

    for i in range(len(dataInAlg)):
        for j in range(len(dataInAlg[0])):
            Gridij[i][j] = (dataInAlg[i][j] - mini[j]) / stepsi[j]

    # print('Gridij', Gridij)

    Grid = [[0] * (GridNum + 1)] * (GridNum + 1)
    Grid = np.array(Grid)

    for i in range(len(Gridij)):
        Grid[Gridij[i][0]][Gridij[i][1]] += 1

    # print(Grid)

    Threshold = len(dataInAlg) / (3 * GridNum)
    Threshold = int(np.ceil(Threshold))
    Threshold = 0
    print('Threshold', Threshold)

    center = []
    distance = 2
    for i in range(len(Grid)):
        for j in range(len(Grid[0])):
            if Grid[i][j] > Threshold:
                a = [i, j, Grid[i][j]]
                center.append(a)

    center = FindTopK(center, clusterNum)

    print('center', center)
    flag = []
    for i in range(len(center)):
        for j in range(i + 1, len(center)):
            if math.sqrt((center[i][0] - center[j][0]) ** 2 + (center[i][1] - center[j][1]) ** 2) < R:
                flag.append(j)
    print('flag', flag)
    # center = np.delete(center, flag, axis=0)
    print('center1', center)

    pointincluster = []

    for i in range(len(center)):
        tempcluster = []
        for j in range(len(Gridij)):
            if (Gridij[j][0] == center[i][0]) & (Gridij[j][1] == center[i][1]):
                tempcluster.append(dataInAlg[j])
        pointincluster.append(tempcluster)

    # pointincluster = np.array(pointincluster)
    # print('pointincluster', pointincluster)

    realcenter = []

    for i in range(len(pointincluster)):
        res = np.mean(pointincluster[i], axis=0)
        realcenter.append(res)

    realcenter = np.array(realcenter)

    print('realcenter', len(realcenter))

    k = len(realcenter)

    # centroids, clusterAssment = KMeans1(data, k, realcenter)

    X = KMeans(init=realcenter, n_clusters=k)
    X.fit(dataInAlg)
    label_pred = X.labels_
    return label_pred

def AGK2(dataInAlg):
    # calculate xsi
    DJ = []
    for i in range(len(dataInAlg[0])):
        DJ.append(np.std(dataInAlg[:, i]) / np.mean(dataInAlg[:, i]))
    DS = 1 / (1 + 1 / len(DJ) * (sum(DJ)))

    m = DS * (len(dataInAlg) ** (1 / len(dataInAlg[0])))
    xsi = int(np.ceil(m))

    rangei, maxi, mini = caculateRange(dataInAlg)

    a = 1

    GridNum = xsi
    GridNum = int(GridNum)
    print("GridNum", GridNum)

    stepsi = []

    for i in range(len(rangei)):
        stepsi.append(rangei[i] / GridNum)

    Gridij = [[0] * len(dataInAlg[0])] * len(dataInAlg)
    Gridij = np.array(Gridij)

    for i in range(len(dataInAlg)):
        for j in range(len(dataInAlg[0])):
            Gridij[i][j] = (dataInAlg[i][j] - mini[j]) / stepsi[j]

    print('Gridij', Gridij)

    Grid = [[0] * (GridNum + 1)] * (GridNum + 1)
    Grid = np.array(Grid)

    for i in range(len(Gridij)):
        Grid[Gridij[i][0]][Gridij[i][1]] += 1

    # print(Grid)

    Threshold = len(dataInAlg) / (3 * GridNum)
    Threshold = int(np.ceil(Threshold))
    print('Threshold', Threshold)

    center = []
    distance = 2
    for i in range(len(Grid)):
        for j in range(len(Grid[0])):
            if Grid[i][j] > Threshold:
                a = [i, j, Grid[i][j]]
                center.append(a)

    print('center', center)

    pointincluster = []

    for i in range(len(center)):
        tempcluster = []
        for j in range(len(Gridij)):
            if (Gridij[j][0] == center[i][0]) & (Gridij[j][1] == center[i][1]):
                tempcluster.append(dataInAlg[j])
        pointincluster.append(tempcluster)

    # pointincluster = np.array(pointincluster)
    # print('pointincluster', pointincluster)

    realcenter = []

    for i in range(len(pointincluster)):
        res = np.mean(pointincluster[i], axis=0)
        realcenter.append(res)

    realcenter = np.array(realcenter)

    print('realcenter', len(realcenter))

    k = len(realcenter)

    # centroids, clusterAssment = KMeans1(data, k, realcenter)

    X = KMeans(init=realcenter, n_clusters=k)
    X.fit(dataInAlg)
    label_pred = X.labels_
    return label_pred