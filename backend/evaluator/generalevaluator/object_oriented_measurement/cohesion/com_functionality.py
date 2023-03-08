from itertools import combinations


def com_chm(methods_id, parameter, variables):
    if len(methods_id) == 1:
        return 1
    if len(methods_id) == 0:
        return -1
    method_pairs = list(combinations(methods_id, 2))
    sim_list = list()
    for pair in method_pairs:
        para_inter, return_inter = _get_inter_set(pair[0], pair[1], parameter, variables)
        para_union, return_union = _get_union_set(pair[0], pair[1], parameter, variables)
        para_weight = _com_weight(para_inter, para_union)
        return_weight = _com_weight(return_inter, return_union)
        if para_weight != -1 and return_weight != -1:
            sim = (para_weight + return_weight) / 2
        elif para_weight == -1 and return_weight != -1:
            sim = return_weight
        elif para_weight != -1 and return_weight == -1:
            sim = para_weight
        sim_list.append(sim)
    return sum(sim_list) / len(sim_list)


def com_chd(methods_id, parameter, variables):
    if len(methods_id) == 1:
        return 1
    if len(methods_id) == 0:
        return -1
    method_pairs = list(combinations(methods_id, 2))
    sim_list = list()
    for pair in method_pairs:
        domain_weight = _get_domain_weight(pair[0], pair[1], parameter, variables)
        if domain_weight != -1:
            sim_list.append(domain_weight)
    return sum(sim_list) / len(sim_list)


def _get_inter_set(method_id1, method_id2, parameter, variables):
    # inter of para type
    para_inter = _get_type(method_id1, parameter, variables) & _get_type(method_id2, parameter, variables)
    # inter of return type
    return_inter = set([_is_exist_raw_type(method_id1, variables)]) & set([_is_exist_raw_type(method_id2, variables)])
    return para_inter, return_inter


def _is_exist_raw_type(method_id, variables):
    if 'rawType' in variables[method_id]:
        return variables[method_id]['rawType']
    return 'void'


def _get_type(method_id, parameter, variables):
    if method_id not in parameter:
        return set(['void'])
    type_list = list()
    for para in parameter[method_id]:
        type_list.append(variables[para]['rawType'])
    return set(type_list)


def _get_union_set(method_id1, method_id2, parameter, variables):
    para_union = _get_type(method_id1, parameter, variables) | _get_type(method_id2, parameter, variables)
    return_union = set([_is_exist_raw_type(method_id1, variables)]) | set([_is_exist_raw_type(method_id2, variables)])
    return para_union, return_union


def _com_weight(inter, union):
    if len(union) == 0:
        return -1
    return len(inter) / len(union)


def _get_domain_weight(method1_id, method2_id, parameter, variables):
    item_set1 = _get_item_set(method1_id, parameter, variables)
    item_set2 = _get_item_set(method2_id, parameter, variables)

    inter_set = item_set1 & item_set2
    union_set = item_set1 | item_set2
    if len(union_set) == 0:
        return -1
    return len(inter_set) / len(union_set)


def _get_item_set(method_id, parameter, variables):
    item_list = list()
    item_list.append(variables[method_id]['name'])
    item_list.append(_is_exist_raw_type(method_id, variables))
    if method_id not in parameter:
        item_list.append('void')
    else:
        for para in parameter[method_id]:
            item_list.append(variables[para]['rawType'])
    return set(item_list)
