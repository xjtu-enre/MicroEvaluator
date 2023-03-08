import argparse
import time

import numpy as np
from sklearn.datasets import load_iris, load_wine, load_breast_cancer
from pyclustering.cluster.clique import clique
from subspaceclustering.cluster.selfrepresentation import ElasticNetSubspaceClustering, SparseSubspaceClusteringOMP


def dataLoad(path, sep, my_type):
    data = []
    with open(path, mode='r', encoding='utf-8') as file:
        for line in file.readlines():
            d = line.strip('\n').split(sep)
            if my_type == 'number':
                data.append(np.float64(d))
            else:
                data.append(d)
        file.close()
        return np.array(data)


def findInWhichCluster(index, clusters):
    k = 0
    for i in range(len(clusters)):
        for j in range(len(clusters[i])):
            if index == clusters[i][j]:
                k = i
    return k

def cliquetest(data):
    # read two-dimensional input data 'Target'
    # data = read_sample(FCPS_SAMPLES.SAMPLE_TARGET)

    # create CLIQUE algorithm for processing
    intervals = 1  # defines amount of cells in grid in each dimension
    threshold = 3  # lets consider each point as non-outlier 这个是阈值密度？
    clique_instance = clique(data, intervals, threshold)
    # start clustering process and obtain results
    clique_instance.process()
    clusters = clique_instance.get_clusters()  # allocated clusters
    # noise = clique_instance.get_noise()  # points that are considered as outliers (in this example should be empty)
    # cells = clique_instance.get_cells()  # CLIQUE blocks that forms grid
    print("Amount of clusters:", len(clusters))
    # 因为每个点都考虑进去了，所以这里中间两聚类加上角上四个聚类就一个有6个聚类了

    label_pred = []

    for index in range(len(data)):
        k = findInWhichCluster(index, clusters)
        label_pred.append(k)

    return label_pred



def resultLabel():
    times = []
    data_path1 = r"/data1/dsy709/untitled1/data/DataForNew/Frogs.txt"
    data_path2 = r"/data1/dsy709/untitled1/data/DataForNew/Frog_label.txt"

    data_path3 = r"/data1/dsy709/untitled1/data/DataForNew/Localization_164860.dat"
    data_path4 = r"/data1/dsy709/untitled1/data/DataForNew/Localization_category.dat"

    data_path5 = r"/data1/dsy709/untitled1/data/DataForNew/Skin_245057.dat"
    data_path6 = r"/data1/dsy709/untitled1/data/DataForNew/Skin_category.dat"

    # data = dataLoad(data_path1, ',', 'number')
    # Y = dataLoad(data_path2, ',', 'number')
    # Y = np.array(Y).T[0]

    data1,Y1 = load_iris(return_X_y= True)
    data2, Y2 = load_wine(return_X_y=True)
    data3, Y3 = load_breast_cancer(return_X_y=True)

    data = []
    Y = []
    clusterNum1 = [3, 3, 2]
    data.append(data1)
    data.append(data2)
    data.append(data3)
    Y.append(Y1)
    Y.append(Y2)
    Y.append(Y3)

    dataPath = []
    dataLabelPath = []
    clusterNum2 = [10, 11, 2]

    dataPath.append(data_path1)
    dataPath.append(data_path3)
    dataPath.append(data_path5)

    dataLabelPath.append(data_path2)
    dataLabelPath.append(data_path4)
    dataLabelPath.append(data_path6)

    for index in range(3):
        start = time.perf_counter()

        # clusterer = hdbscan.RobustSingleLinkage(cut=0.125, k=clusterNum1[index])
        # label_pred = clusterer.fit_predict(data[index])

        # label_pred = cliquetest(data[index])

        # model = ElasticNetSubspaceClustering(n_clusters=clusterNum1[index], algorithm='lasso_lars', gamma=50).fit(data[index])

        model = SparseSubspaceClusteringOMP(n_clusters=clusterNum1[index]).fit(data[index])
        label_pred = model.labels_

        end = time.perf_counter()
        temp = end - start
        times.append(temp)

        print(times)


    for index in range(3):
        start = time.perf_counter()

        data = dataLoad(dataPath[index], ',', 'number')
        Y = dataLoad(dataLabelPath[index], ',', 'number')
        Y = np.array(Y).T[0]

        # clusterer = hdbscan.RobustSingleLinkage(cut=0.125, k=clusterNum2[index])
        # label_pred = clusterer.fit_predict(data)

        # label_pred = cliquetest(data)

        # model = ElasticNetSubspaceClustering(n_clusters=clusterNum2[index], algorithm='lasso_lars', gamma=50).fit(data)

        model = SparseSubspaceClusteringOMP(n_clusters=clusterNum2[index]).fit(data)

        label_pred = model.labels_

        end = time.perf_counter()
        temp = end - start
        times.append(temp)

        print(times)

    # print('adjusted_rand_score', metrics.adjusted_rand_score(Y, label_pred))
    # print('adjusted_mutual_info_score', metrics.adjusted_mutual_info_score(Y, label_pred))
    # print('fowlkes_mallows_score', metrics.fowlkes_mallows_score(Y, label_pred))
    print(times)


def main():

    resultLabel()


if __name__ == '__main__':
    main()
