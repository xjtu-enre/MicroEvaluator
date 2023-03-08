import os
from pathlib import Path

import json


def get_json_file(path1, path2, result_path):
    # print(path1)
    # print(path2)
    # print(result_path)
    # for root, dirs, files in os.walk(path1):
    #     print(root)
    #     for file in files:
    #         print(file)
    # file_path1 = os.path.join(root, file)
    # file_path2 = Path(os.path.join(path2, file))
    # if not file_path2.is_file():
    #     continue
    json_dict1 = read_json(path1)
    json_dict2 = read_json(path2)
    json_deal(json_dict1, json_dict2, result_path)


def read_json(file_path):
    with open(file_path, 'r') as f:
        json_dict = json.load(f)
    return json_dict


def json_deal(json_dict1, json_dict2, path):
    # print(path)
    result = list()
    variables1 = json_dict1['variables']
    variables2 = json_dict2['variables']
    cell1 = json_dict1['cells']
    cell2 = json_dict2['cells']

    contain1 = dict()
    for c1 in cell1:
        if 'Contain' in c1['values']:
            if c1['src'] not in contain1:
                contain1[c1['src']] = list()
            contain1[c1['src']].append(c1['dest'])

    contain2 = dict()
    for c2 in cell2:
        if 'Contain' in c2['values']:
            if c2['src'] not in contain2:
                contain2[c2['src']] = list()
            contain2[c2['src']].append(c2['dest'])

    read_variables1(variables1, variables2, contain1, contain2, result)
    read_variables2(variables1, variables2, result)
    # print(result)
    write_to_json(result, path)


def read_variables1(variables1, variables2, contain1, contain2, result):
    hash_map2 = dict()
    for var2 in variables2:
        if not var2['external'] and var2['qualifiedName'] + var2['category'] not in hash_map2:
            hash_map2[var2['qualifiedName'] + var2['category']] = var2

    for var1 in variables1:
        if not var1['external'] and (
                var1['category'] == 'File' or var1['category'] == 'Class' or var1['category'] == 'Interface' or var1[
            'category'] == 'Method'):
            if (var1['qualifiedName'] + var1['category']) in hash_map2:
                # 对比两个对象的children信息，如果全部无变化就为nochange，有任何变化就为modify(True:modify False:nochange)
                com_res = compare(var1['id'], hash_map2[var1['qualifiedName'] + var1['category']]['id'], variables1,
                                  variables2, contain1, contain2)
                if com_res:
                    var1['status'] = 'modify'
                else:
                    var1['status'] = 'nochange'
            else:
                var1['status'] = 'delete'
            result.append(var1)


def read_variables2(variables1, variables2, result):
    hash_map1 = dict()
    for var1 in variables1:
        if not var1['external'] and var1['qualifiedName'] + var1['category'] not in hash_map1:
            hash_map1[var1['qualifiedName'] + var1['category']] = var1

    for var2 in variables2:
        if not var2['external'] and (
                var2['category'] == 'File' or var2['category'] == 'Class' or var2['category'] == 'Interface' or var2[
            'category'] == 'Method'):
            if (var2['qualifiedName'] + var2['category']) not in hash_map1:
                var2['status'] = 'insert'
                result.append(var2)


def write_to_json(content, path):
    with open(path, 'w') as f:
        json.dump(content, f)


def compare(var1_id, var2_id, variables1, variables2, contain1, contain2):
    if var1_id not in contain1 and var2_id not in contain2:
        return False
    if (var1_id not in contain1 and var2_id in contain2) or (var1_id in contain1 and var2_id not in contain2) or len(
            contain1[var1_id]) != len(contain2[var2_id]):
        return True
    for id1 in contain1[var1_id]:
        for id2 in contain2[var2_id]:
            if variables1[id1]['qualifiedName'] == variables2[id2]['qualifiedName'] and variables1[id1]['category'] == \
                    variables2[id2]['category']:
                return compare(id1, id2, variables1, variables2, contain1, contain2)
            else:
                return True

#
# if __name__ == '__main__':
#     print(time.localtime())
#     get_json_file(r'C:\Users\20463\Desktop\android\android_11.0.0_r2_enre',
#                   r'C:\Users\20463\Desktop\android\android_12.0.0_enre')
#     print(time.localtime())
