# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import numpy.matlib
import copy
import random as rnd
from scipy.spatial import distance
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
from scipy.spatial import distance
from scipy.spatial.distance import cdist
import sys
from sklearn import datasets
from sklearn.datasets import load_iris
from sklearn.datasets import load_wine
from sklearn.datasets import load_breast_cancer
import matplotlib.pyplot as plt
from sklearn import metrics
import time


# iris = load_iris()
# X = iris.data[:,2:] ##表示我们只取特征空间中的后两个维度


def SMKM(D, k, start):
    ####################
    # INPUT:
    # D: data set, k= number of clusters
    # start=0 -> Forgy K-means
    # start=1 -> K-means++
    ####################
    print('Re_start', 'Error', 'Dist', 'Lloyd_It')
    #####################
    # Output is printed in the following order:
    # 1) Number of the re-start, 2) K-means error, 3) Distances computed, 4) Accumulated number of Lloyd Iterations.
    #####################
    n = D.shape[0]
    d = D.shape[1]
    i = 0
    STOP = False
    DC3 = 0
    ITU = 0
    while STOP == False:
        i += 1
        if i == 1:
            if start == 0:
                k_means = KMeans(init='random', n_clusters=k, n_init=1)
            if start == 1:
                k_means = KMeans(init='k-means++', n_clusters=k, n_init=1)
                DC3 = DC3 + (k - 1) * (n - (k / 2.0))
        else:
            k_means = KMeans(init=C03, n_clusters=k, n_init=1)

        k_means.fit(D)

        DC3 = k_means.n_iter_ * k * n + DC3
        C03 = k_means.cluster_centers_
        # print(C03)
        ITU = ITU + k_means.n_iter_
        Jin03 = sum(numpy.min(cdist(D, C03, 'sqeuclidean'), axis=1))
        #############
        if i == 1:
            Jin0 = Jin03 + 1
            #############
        if Jin03 >= Jin0:
            STOP = True
            print(i, Jin03, DC3, ITU)
        else:
            print(i, Jin03, DC3, ITU)
            Jin0 = Jin03
            Desc = np.zeros(k)
            tt = 1
            U = np.array([np.where(k_means.labels_ == j) for j in range(k)])
            # print('U',U)
            f = np.array([sum(cdist(D[U[j][0]], C03[j].reshape(1, -1), 'sqeuclidean')) for j in range(k)])
            # print('f',U[1][0])
            lU = np.array([len(np.where(k_means.labels_ == j)[0]) for j in range(k)])
            # print('lU', lU)
            CC = np.array([np.array([C03[0], C03[0]]) for iI in range(k)])
            l0C = np.zeros(k)
            l1C = np.zeros(k)
            for j in range(k):
                X = D[U[j][0]]

                if len(X) > 1:

                    k_meansINT = KMeans(init='k-means++', n_clusters=2, n_init=1)
                    k_meansINT.fit(X)
                    DC3 = k_meansINT.n_iter_ * 2 * len(X) + DC3 + len(X)

                    CC[j] = np.array([k_meansINT.cluster_centers_[0], k_meansINT.cluster_centers_[1]])
                    l0C[j] = len(np.where(k_meansINT.labels_ == 0)[0])
                    l1C[j] = len(np.where(k_meansINT.labels_ == 1)[0])
                    Desc[j] = k_meansINT.inertia_ - f[j]

                else:
                    Desc[j] = 0

            kk = np.argmin(Desc)
            C03 = np.delete(C03, kk, 0)
            lU = np.delete(lU, kk, 0)
            C03 = np.vstack((C03, CC[kk][0]))
            C03 = np.vstack((C03, CC[kk][1]))
            lU = np.hstack((lU, l0C[kk]))
            lU = np.hstack((lU, l1C[kk]))
            Z = cdist(C03, C03, 'sqeuclidean')
            tt = 0
            Z0 = copy.deepcopy(Z)
            for j in range(k):
                for m in range(j, k + 1):
                    t = (lU[j] * lU[m]) / (lU[j] + lU[m])
                    # print 't:',t
                    Z0[j][m] = Z[j][m] * t
                    Z0[m][j] = 0
            Z0[k - 1][k] = 0
            ind = np.where(Z0 == np.min(Z0[np.nonzero(Z0)]))
            j = ind[0][0]
            m = ind[1][0]
            C03[j] = (lU[j] * C03[j] + lU[m] * C03[m]) / (lU[j] + lU[m])
            C03 = np.delete(C03, m, 0)
            Jin = sum(numpy.min(cdist(D, C03, 'sqeuclidean'), axis=1))
    plt.scatter(C03[:, 0], C03[:, 1], c="yellow", marker='o', label='see')
    label_pred = k_means.labels_

    return label_pred
