import numpy as np
import networkx as nx
import math


class Chameleon:
    W = None # weight矩阵(方阵)
    Conn = None # 连接矩阵(方阵)
    clusters = None
    MI = 0 # 综合指数
 
    # 构造函数，初始化变量
    def __init__(self, datanum, mi):
        self.W = np.ones((datanum, datanum))
        self.Conn = np.zeros((datanum, datanum))
        self.datanum = datanum
        self.clusters = []
        self.MI = mi
        self.inter_EC = None
    
    # 构造weight矩阵。根据两点间距离的倒数计算两点的相似度，作为连接权重
    def buildWeightMatrix(self, data):
        for i in range(data.shape[0]):
            row = data[i]
            temp = data - row
            temp = np.multiply(temp, temp)
            temp = np.sum(temp, axis=1)
            self.W[i] = 1 / np.sqrt(temp)
            self.W[i][i] = 1.0
 
    # CHAMELEON第一阶段，按照K(包括自己)最邻近建立较小的子簇
    def buildSmallCluster(self):
        K = 2  # 2最邻近，这里面包括它自己
        for i in range(self.W.shape[0]):
            row = self.W[i]
            index = np.argsort(row)
            index = index[-K:]
            index = list(index)
            self.Conn[i, index] = 1
            self.Conn[i][i] = 0
        
        # 根据连接矩阵构造连通子图
        nodes = []
        edges = []
        for i in range(len(self.Conn)):
            nodes.append(i)
            for j in range(len(self.Conn)):
                if self.Conn[i][j] == 1:
                    edges.append((i, j))
        
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
 
        # 极大连通子图
        C = sorted(nx.connected_components(G), key=len, reverse=True)
        for c in C:
            cluster = []
            for node in c:
                cluster.append(node)
            self.clusters.append(cluster)

    # 打印子簇
    def printClusters(self):
        for i in range(len(self.clusters)):
            print("以下数据点属于第" + str(i) + "簇：")
            item = self.clusters[i]
            print(item)
  
    # CHAMELEON第二阶段，合并相对互联度RI和相对紧密度RC都较高的簇
    def cluster(self):
        self.interConnectivity()
        l = len(self.clusters)
        end = True
        i = 0
        while i < l:
            EC_i = self.inter_EC[i]
            j = i + 1
            while j < l:
                EC_j = self.inter_EC[j]
                vec1 = self.clusters[i]
                vec2 = self.clusters[j]
                EC = 0.0
                for k in range(len(vec1)):
                    for m in range(len(vec2)):
                        EC += self.W[vec1[k]][vec2[m]] 
                    
                RI = 2 * EC / (EC_i + EC_j)
                RC = (len(vec1) + len(vec2)) * EC / (len(vec2) * EC_i + len(vec1) * EC_j)
                if RI * math.pow(RC, 2) > self.MI:
                    self.mergeClusters(i, j)
                    l -= 1
                    end = False
                    break
                j = j + 1
            i = i + 1
        # 递归合并子簇
        if not end:
            self.cluster()
        return self.clusters
            
    def interConnectivity(self):
        l = len(self.clusters)
        self.inter_EC = [0 for i in range(l)]
        for i in range(l):
            vec = self.clusters[i]
            for j in range(len(vec)):
                for k in range(len(vec)):
                    self.inter_EC[i] += self.W[vec[j]][vec[k]]
 
    # 把簇b合并到簇a里面去
    def mergeClusters(self, a, b):
        item = self.clusters[b]
        self.clusters.pop(b)
        self.clusters[a].extend(item)


def getCoChangeCluster(data):
    cham = Chameleon(data.shape[0], 0.3)
    cham.buildWeightMatrix(data)
    cham.buildSmallCluster()
    cluster = cham.cluster()

    return cluster