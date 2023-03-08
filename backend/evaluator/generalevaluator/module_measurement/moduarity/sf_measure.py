import numpy as np
import csv


from evaluator.generalevaluator.module_measurement.moduarity.chameleon import getCoChangeCluster


def get_spread_and_focus(cmt_path, module_info, variables):
    # create coChangeGraph
    commit, module_classes = read_commit(cmt_path, module_info, variables)
    co_change_graph, vertexes = _get_co_change_graph(commit)
    # get coChangeCluster
    co_change_cluster = getCoChangeCluster(co_change_graph)
    # transfer pathname to qualifiedName
    co_change_cluster = _deduplication(co_change_cluster, vertexes)
    # compete focus and spread
    focus, spread = _compete_spread_and_focus(co_change_cluster, module_classes)
    focus_dic, spread_dic = _get_focus_and_spread_dict(focus, spread, list(module_classes.keys()))

    return focus_dic, spread_dic, module_classes, commit


def get_module_classes(module_info, variables, all_classes):
    result = dict()
    for module_id in module_info:
        result[variables[module_id]['qualifiedName']] = list()
        for class_id in module_info[module_id]:
            # if variables[class_id]['File'] in all_classes:
            result[variables[module_id]['qualifiedName']].append(variables[class_id]['File'])
    return result


def _get_focus_and_spread_dict(focus, spread, modules):
    focus_dic = dict()
    spread_dic = dict()
    for index in range(0, len(modules)):
        focus_dic[modules[index]] = focus[index]
        spread_dic[modules[index]] = spread[index]
        # focus_dic[modules[index]] = 0
        # spread_dic[modules[index]] = 0

    return focus_dic, spread_dic


def _deduplication(co_change_cluster, vertexes):
    final_co_change_cluster = list()
    for index1 in range(0, len(co_change_cluster)):
        temp_cluster = list()
        for index2 in range(0, len(co_change_cluster[index1])):
            module_name = vertexes[co_change_cluster[index1][index2]]
            if module_name not in temp_cluster:
                temp_cluster.append(module_name)
        final_co_change_cluster.append(temp_cluster)
    return final_co_change_cluster


def _get_co_change_graph(commit):
    vertexes = list(commit.keys())
    commit_matrix = [[0] * len(commit) for _ in range(len(commit))]
    # commit_matrix
    for index1 in range(0, len(vertexes)):
        for index2 in range(0, len(vertexes)):
            if vertexes[index2] in commit[vertexes[index1]]:
                commit_matrix[index1][index2] = commit[vertexes[index1]][vertexes[index2]]
            else:
                commit_matrix[index1][index2] = 0

    return np.array(commit_matrix), np.array(vertexes)


def _compete_spread_and_focus(co_change_cluster, module_classes):
    # coChangeCluster = [{'a', 'b'}, {'c'}, {'d', 'e', 'f'}]
    # service2Class = {'0': ['a'], '1': ['f'], '2': ['d'], '3': ['c', 'b', 'e']}
    focus = list()
    spread = list()
    for module_name in module_classes:
        temp_spread = 0
        temp_focus = 0
        for cluster in co_change_cluster:
            # if cluster & service != null, then temp_count += 1
            temp_count = 0
            flag = False
            for item1 in module_classes[module_name]:
                if item1 in cluster:
                # for item2 in cluster:
                #     if trans_to_path(item1) in item2:
                    if not flag:
                        flag = True
                        temp_spread = temp_spread + 1
                    temp_count = temp_count + 1
            temp_focus = temp_focus + (temp_count / len(module_classes[module_name])) * (temp_count / len(cluster))
        focus.append(float(format(temp_focus, '.4f')))
        spread.append(float(format(temp_spread / len(module_classes), '.4f')))
    # 对spread值进行归一化
    # spreadResult = spreadNormalized(spread)
    return focus, spread


def trans_to_path(name):
    return name.replace('.', '/')


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


def read_commit(file_name, module_info, variables):
    all_classes = list()
    commit_dic = dict()
    with open(file_name, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [class1, class2, commit] = each
            class1 = class1.replace('\\', '/')
            class2 = class2.replace('\\', '/')
            if class1 not in commit_dic:
                commit_dic[class1] = dict()
                all_classes.append(class1)
            commit_dic[class1][class2] = int(commit)

    # module contains classes
    module_classes = get_module_classes(module_info, variables, all_classes)

    return commit_dic, module_classes


