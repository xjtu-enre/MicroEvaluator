import json
import os
import numpy as np
from evaluator.utils.common import *
from evaluator.utils.scoreutil import *
from operator import itemgetter
from project.models import *
from evaluator.generalevaluator.function_file import *


def load_json():
    base_path = './featureextractor/data/'
    flag = 0
    json_list = list()
    for root, dirs, files in os.walk(base_path):
        if flag == 1:
            break
        for dir in dirs:
            measure_file = os.path.join(root, dir + '/measure_result.json')
            with open(measure_file, 'r', encoding='utf-8') as f:
                json_list.append(json.load(f, strict=False))
        flag = 1
    return json_list


def load_measure_json(project_name):
    pro_id = Project.objects.filter(projectname=project_name).first().id
    vers = VersionProject.objects.filter(project=pro_id).all()
    base_path = './featureextractor/data/' + project_name
    measure_list = list()
    dep_list = list()
    for ver in vers:
        measure_path = base_path +  '/' + ver.version + '/measure_result.json'
        dep_path = base_path +  '/' + ver.version + '/dep.json'
        with open(measure_path, 'r', encoding='utf-8') as f:
            measure_list.append(json.load(f, strict=False))
        with open(dep_path, 'r', encoding='utf-8') as f:
            dep_list.append(json.load(f, strict=False))

    result = list()
    measure_diff = compare_diff(measure_list, dep_list, dict(), base_path)
    result.append(list(measure_diff.keys()))
    result.append(MODULE_METRICS)

    # 遍历两个版本的变化写入热力图数据
    index_matrix = [['' for col in range(len(MODULE_METRICS))] for row in range(len(measure_diff))]
    normalized_result = [['' for col in range(len(MODULE_METRICS))] for row in range(len(measure_diff))]
    index = 0
    for pacage_name in measure_diff:
        index_matrix[index][0] = float(measure_diff[pacage_name]['scoh'])
        index_matrix[index][1] = float(measure_diff[pacage_name]['scop'])
        index_matrix[index][2] = float(measure_diff[pacage_name]['odd'])
        index_matrix[index][3] = float(measure_diff[pacage_name]['idd'])
        index_matrix[index][4] = float(measure_diff[pacage_name]['spread'])
        index_matrix[index][5] = float(measure_diff[pacage_name]['focus'])
        index_matrix[index][6] = float(measure_diff[pacage_name]['icf'])
        index_matrix[index][7] = float(measure_diff[pacage_name]['ecf'])
        index_matrix[index][8] = float(measure_diff[pacage_name]['rei'])
        index_matrix[index][9] = float(measure_diff[pacage_name]['DSM'])
        index += 1

    # axis为0时求每列最值，为1时求每行最值
    max = np.amax(index_matrix, axis=0)
    min = np.amin(index_matrix, axis=0)
    temp_change = list()
    for index1 in range(0, len(index_matrix)):
        for index2 in range(0, len(index_matrix[index1])):
            # scoh越大越好
            if index2 == 0 or index2 == 5 or index2 == 6:
                normalized_result[index1][index2] = float(
                    format((index_matrix[index1][index2] - min[index2]) / (max[index2] - min[index2]), '.4f'))
            # 其他指标越小越好
            else:
                normalized_result[index1][index2] = float(
                    format((max[index2] - index_matrix[index1][index2]) / (max[index2] - min[index2]), '.4f'))
            temp_change.append([index1, index2, normalized_result[index1][index2]])
    result.append(temp_change)
    return result


def get_project_data(json_list):
    project_metric_data = list()
    module_metric_list = list()
    # project_metric_data.append(PROJECT_METRICS_LEVEL)
    # module_metric_list.append(MODULE_METRIC_LEVEL)
    pro_index = 0
    loc = list()
    for project in json_list:
        pro_metrics = project[list(project.keys())[0]]
        temp_pro = list()
        # temp_pro.append(VersionProject.objects.filter(id=int(list(project.keys())[0])))
        loc.append(VersionProject.objects.filter(id=int(list(project.keys())[0])).first().loc)
        temp_pro.extend(list(itemgetter(*PROJECT_METRICS)(pro_metrics)))
        project_metric_data.append(temp_pro)
        module_index = 0
        for module in pro_metrics['modules']:
            module_metric_list.append(list(itemgetter(*MODULE_METRICS)(pro_metrics['modules'][module])))
            module_index += 1
        pro_index += 1
    # 计算及添加score
    project_metric_data = np.insert(project_metric_data, 0, values=loc, axis=1)
    normalized_result, score_result = get_score(project_metric_data, PROJECT_METRICS)
    project_metric_data = np.insert(project_metric_data, 1, values=score_result, axis=1)
    #  对库中所有项目指标及模块进行分级
    project_metric_data = com_level(project_metric_data)

    return project_metric_data.tolist(), module_metric_list


def com_level(project_metric_data):
    project_metric_data = np.insert(project_metric_data, 1, values=get_level(project_metric_data[:0], 'loc'), axis=1)
    project_metric_data = np.insert(project_metric_data, 3, values=get_level(project_metric_data[:2], 'score'), axis=1)
    project_metric_data = np.insert(project_metric_data, 5, values=get_level(project_metric_data[:4], 'SMQ'), axis=1)
    project_metric_data = np.insert(project_metric_data, 7, values=get_level(project_metric_data[:6], 'ODD'), axis=1)
    project_metric_data = np.insert(project_metric_data, 9, values=get_level(project_metric_data[:8], 'IDD'), axis=1)
    project_metric_data = np.insert(project_metric_data, 11, values=get_level(project_metric_data[:10], 'SPREAD'),
                                    axis=1)
    project_metric_data = np.insert(project_metric_data, 13, values=get_level(project_metric_data[:12], 'FOUCUS'),
                                    axis=1)
    project_metric_data = np.insert(project_metric_data, 15, values=get_level(project_metric_data[:14], 'ICF'), axis=1)
    project_metric_data = np.insert(project_metric_data, 17, values=get_level(project_metric_data[:16], 'ECF'), axis=1)
    project_metric_data = np.insert(project_metric_data, 19, values=get_level(project_metric_data[:18], 'REI'), axis=1)
    return project_metric_data


def get_level(value, itype):
    level_list = list()
    [value_q1, value_q2, value_q3, value_ulim, value_llim] = _get_percent(value)
    for item in value:
        if itype in MIN_METRICS:
            if item > value_q3:
                level_list.append('D')
            elif item > value_q2:
                level_list.append('C')
            elif item > value_q1:
                level_list.append('B')
            else:
                level_list.append('A')
        else:
            if item > value_q3:
                level_list.append('A')
            elif item > value_q2:
                level_list.append('B')
            elif item > value_q1:
                level_list.append('C')
            else:
                level_list.append('D')
    return level_list


def _get_percent(value):
    # 使用箱线图计算行数、评分的1/4、1/2、3/4数
    [value_q1, value_q2, value_q3, value_ulim, value_llim] = get_percent(value)

    return [value_q1, value_q2, value_q3, value_ulim, value_llim]


def get_percent(input):
    # 转换普通列表为数字型列表，以防出错
    input = np.array(input, dtype=np.float)
    # 获取箱体图特征
    percentile = np.percentile(input, (25, 50, 75), interpolation='midpoint')
    # 以下为箱线图的五个特征值
    Q1 = percentile[0]  # 上四分位数
    Q2 = percentile[1]  # 中位数
    Q3 = percentile[2]  # 下四分位数
    IQR = Q3 - Q1  # 四分位距,即盒子的长度
    ulim = Q3 + 1.5 * IQR  # 上限 非异常范围内的最大值
    llim = Q1 - 1.5 * IQR  # 下限 非异常范围内的最小值
    # print(percentile)

    return Q1, Q2, Q3, ulim, llim


if __name__ == '__main__':
    json_list = load_json()
    project_metric_data, module_list = get_project_data(json_list)
