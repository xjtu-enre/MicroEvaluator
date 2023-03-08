#! /usr/bin/env python3

import json
import os
import csv
from pathlib import Path
from collections import defaultdict


def read_entities(entities_diff_path):
    status = defaultdict(lambda: defaultdict(str))
    with open(entities_diff_path, "r") as f:
        data = json.load(f)
        for entity in data:
            key = entity["qualifiedName"] + "%" + str(entity["id"])
            status[key] = entity["status"]
    return status


def read_modules(dep_path):
    # modules = os.listdir(path)
    reduce_dt = defaultdict(lambda: defaultdict(int))
    variables_dt = defaultdict(lambda: defaultdict(int))
    relations_dt = defaultdict(lambda: defaultdict(list))
    relations_qname_dt = defaultdict(lambda: defaultdict(str))
    # for module in modules:
    #     print("reading {}...".format(os.path.join(path, module)))
    with open(dep_path, "r") as f:
        data = json.load(f)
        if "cells" not in data or "variables" not in data:
            return relations_dt, variables_dt, relations_qname_dt, reduce_dt
        variables_data = data["variables"]
        for var in variables_data:
            if var["external"]:
                continue
            variables_dt[int(var["id"])] = var["qualifiedName"]
        cells_data = data["cells"]
        for cell in cells_data:
            key = str(cell["src"]) + "%" + str(cell["dest"])
            qname_key = variables_dt[int(cell["src"])] + "%" + variables_dt[int(cell["dest"])]
            relations_qname_dt[qname_key] = key
            for relation in cell["values"]:
                if len(cell["values"]) > 1:
                    continue
                value = {"relation": relation, "count": int(cell["values"][relation])}
                if relation not in reduce_dt:
                    reduce_dt[relation] = 0
                reduce_dt[relation] += value["count"]
                # reduce_dt["base"][relation] += value["count"]
                if key not in relations_dt:
                    relations_dt[key] = list()
                relations_dt[key].append(value)
    return relations_dt, variables_dt, relations_qname_dt, reduce_dt, variables_data


def compare(relations1, variables1, relations2, variables2, qname_dt1, qname_dt2, entities_status):
    relations_dt = list()
    for key1, lst1 in relations1.items():
        sp1 = key1.split("%")
        src1 = int(sp1[0])
        dest1 = int(sp1[1])
        qname1 = variables1[src1]
        qname2 = variables1[dest1]
        qname_key1 = str(qname1) + "%" + str(qname2)
        if qname_key1 not in qname_dt2:
            for value1 in lst1:
                relation = value1["relation"]
                value_dt = {relation: value1["count"]}
                value = {"src": src1, "values": value_dt, "status": "delete", "dest": dest1}
                relations_dt.append(value)
            continue
        lst2 = relations2[qname_dt2[qname_key1]]
        for value1 in lst1:
            relations_matched = False
            for value2 in lst2:
                if value1["relation"] == value2["relation"]:
                    relation_matched = True
                    operation = ""
                    if value1["count"] == value2["count"]:
                        if entities_status[qname1] == "nochange" and entities_status[qname2] == "nochange":
                            operation = "nochange"
                        else:
                            operation = "modify"
                    elif value1["count"] < value2["count"]:
                        operation = "delete"
                    else:
                        operation = "insert"
                    relation = value1["relation"]
                    value_dt = {relation: value1["count"]}
                    value = {"src": src1, "values": value_dt, "status": operation, "dest": dest1}
                    relations_dt.append(value)
                    break
            if not relation_matched:
                relation = value1["relation"]
                value_dt = {relation: value1["count"]}
                value = {"src": src1, "values": value_dt, "status": "delete", "dest": dest1}
                relations_dt.append(value)
        for value2 in lst2:
            relation_matched = False
            for value1 in lst1:
                if value1["relation"] == value2["relation"]:
                    relation_matched = True
                    break
            if relation_matched == False:
                relation = value2["relation"]
                value_dt = {relation: value2["count"]}
                value = {"src": src1, "values": value_dt, "status": "insert", "dest": dest1}
                relations_dt.append(value)
    for key2, lst2 in relations2.items():
        sp2 = key2.split("%")
        src2 = int(sp2[0])
        dest2 = int(sp2[1])
        qname3 = variables2[src2]
        qname4 = variables2[dest2]
        qname_key2 = str(qname3) + "%" + str(qname4)
        if qname_key2 not in qname_dt1:
            for value2 in lst2:
                relation = value2["relation"]
                value_dt = {relation: value2["count"]}
                value = {"src": src2, "values": value_dt, "status": "insert", "dest": dest2}
                relations_dt.append(value)
    return relations_dt


def write_csv(reduce_dt, name):
    cdata = defaultdict(list)
    relations = [
        "Import",
        "Inherit",
        "Implement",
        "Parameter",
        "Call",
        "Use",
        "Cast",
        "Set",
        "Modify",
        "Call non-dynamic",
    ]
    cdata = defaultdict(list)
    for module, ddt in reduce_dt.items():
        for relation in relations:
            if relation not in ddt:
                cdata[module].append(0)
            else:
                cdata[module].append(ddt[relation])
    with open(name, "w") as f:
        writer = csv.writer(f)
        for module, lst in cdata.items():
            writer.writerow([module[:-9]] + lst)
    return


def dump_modules(relations_dt, variables_data2, result_path):
    relations_dt = format_relation(relations_dt, variables_data2)
    with open(result_path, "w") as f:
        json.dump(relations_dt, f, indent=4)


def format_relation(relations_dt, variables_data2):
    result = dict()
    for item in relations_dt:
        # 判断src是否为File，若为File，那么在输出时直接输出File
        if 'category' not in variables_data2[item['src']] or 'File' not in variables_data2[item['src']]['category']:
            continue
        if list(item['values'].keys())[0] not in result:
            result[list(item['values'].keys())[0]] = dict()
        if item['status'] not in result[list(item['values'].keys())[0]]:
            result[list(item['values'].keys())[0]][item['status']] = list()
        result[list(item['values'].keys())[0]][item['status']].append(
            {'src': variables_data2[item['src']]['File'], 'dest': variables_data2[item['dest']]['qualifiedName']})

    return result


def get_diff_relation(dep1, dep2, entity_diff, result_path):
    print('dep1', dep1)
    print('dep2', dep2)
    print('entity_diff', entity_diff)
    print('result_path', result_path)
    relations1, variables1, qname_dt1, reduce_dt1, variables_data1 = read_modules(dep1)
    relations2, variables2, qname_dt2, reduce_dt2, variables_data2 = read_modules(dep2)
    entities_status = read_entities(entity_diff)
    relations_dt = compare(relations1, variables1, relations2, variables2, qname_dt1, qname_dt2, entities_status)
    # 只输出File相关的依赖diff，因为在后面显示时需要匹配的都是filename
    dump_modules(relations_dt, variables_data2, result_path)



if __name__ == '__main__':
    get_diff_relation(r'E:\MicroEvaluator\backend\featureextraction/data/lineage/lineage-16.0/lineage.json',
                      r'E:\MicroEvaluator\backend\featureextraction/data/lineage/lineage-17.1/lineage.json',
                      r'E:\MicroEvaluator\backend\featureextraction/data/lineage/entities-out.json',
                      r'E:\MicroEvaluator\backend\featureextraction/data/lineage/relation.json')
