import numpy as np


def boxFeature(input, index_type):
    result = []
    if len(input) == 0:
        return result
    # print(input)
    # print(index_type)
    # maxfeature代表这些特征值越大越不好，minfeature代表这些指标越小越不好
    maxfeature = {'ifn', 'rei', 'idd', 'odd', 'scop', 'ccop'}
    minfeature = {'chm', 'chd', 'ccoh', 'scoh'}
    [Q1, Q2, Q3, ulim, llim] = get_percent(input)
    # #获取箱体图特征
    # percentile = np.percentile(input, (25, 50, 75), interpolation='midpoint')
    # #以下为箱线图的五个特征值
    # Q1 = percentile[0] #上四分位数
    # Q3 = percentile[2] #下四分位数
    # IQR = Q3 - Q1 #四分位距,即盒子的长度
    # ulim = Q3 + 1.5 * IQR #上限 非异常范围内的最大值
    # llim = Q1 - 1.5 * IQR #下限 非异常范围内的最小值

    # 判断当前传进来的指标是要取最大还是最小：利用是否存在大小指标集合中来定
    # 若最大，那么将异常的微服务放入到一个最大异常对象中；
    # 若最小，那么将异常的微服务放入到一个最小异常对象中。
    if index_type in maxfeature:
        for index in range(0, len(input)):
            if input[index] > ulim:
                result.append(index)

    if index_type in minfeature:
        for index in range(0, len(input)):
            if input[index] < llim:
                result.append(index)

    return result


def get_percent(input):
    # 转换普通列表为数字型列表，以防出错
    input = np.array(input, dtype=np.float)
     #获取箱体图特征
    percentile = np.percentile(input, (25, 50, 75), interpolation='midpoint')
    #以下为箱线图的五个特征值
    Q1 = percentile[0] #上四分位数
    Q2 = percentile[1] #中位数
    Q3 = percentile[2] #下四分位数
    IQR = Q3 - Q1 #四分位距,即盒子的长度
    ulim = Q3 + 1.5 * IQR #上限 非异常范围内的最大值
    llim = Q1 - 1.5 * IQR #下限 非异常范围内的最小值
    # print(percentile)

    return Q1, Q2, Q3, ulim, llim