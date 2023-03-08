import csv
import os
import numpy as np


# 传入指标矩阵和权重数组，计算最后的综合评分
def get_score(index_matrix, weight, type_names):
    # max_feature：越大越好；min_feature:越小越好
    max_feature = {'chm', 'chd', 'icf', 'scoh', 'ccoh', 'focus'}
    min_feature = {'ifn', 'rei', 'idd', 'odd', 'ecf', 'scop', 'ccop', 'DSM', 'spread'}
    normalized_result = [['' for col in range(len(type_names))] for row in range(len(index_matrix))]

    # axis为0时求每列最值，为1时求每行最值
    max = np.amax(index_matrix, axis=0)
    min = np.amin(index_matrix, axis=0)

    # 求出归一化指标值和最终的综合评分
    for index1 in range(0, len(index_matrix)):
        for index2 in range(0, len(index_matrix[index1])):
            # 最大最小值相等时，即所有微服务在这个指标表现值一样
            # if max[index2] - min[index2] == 0:
            #     normalized_result[index1][index2] = 0
            # else:
            # 遗留问题：对于整组数据全相等的不能简单处理为结果为0
            if type_names[index2] in min_feature:
                if max[index2] - min[index2] == 0:
                    # 一般情况下出现这种现象的情况：所有ifn为0或者1、所有scop全为0
                    normalized_result[index1][index2] = 1
                    continue
                # 数据标准化归一化
                normalized_result[index1][index2] = float(
                    format((max[index2] - index_matrix[index1][index2]) / (max[index2] - min[index2]), '.4f'))
            if type_names[index2] in max_feature:
                if max[index2] - min[index2] == 0:
                    # 若其中指标取值全为1，那么最后评分应该为1
                    if max[index2] == 1:
                        normalized_result[index1][index2] = 1
                    elif max[index2] == 0:
                        normalized_result[index1][index2] = 0
                    else:
                        normalized_result[index1][index2] = max[index2]
                    continue
                normalized_result[index1][index2] = float(
                    format((index_matrix[index1][index2] - min[index2]) / (max[index2] - min[index2]), '.4f'))

    # 求最终评分数组
    score_result = np.dot(normalized_result, weight)
    # 给予每个微服务相同的权重，并将最终结果存入数据库
    score = sum(score_result) / len(score_result)
    return [normalized_result,  [i[0] for i in score_result]]
