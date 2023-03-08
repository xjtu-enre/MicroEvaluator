from evaluator.generalevaluator.module_measurement.moduarity.sf_measure import read_commit, get_module_classes, trans_to_path


def get_icf_ecf_rei(module_classes, commit):
    icf_dic, ecf_dic, rei_dic = _com_value(commit, module_classes)
    return icf_dic, ecf_dic, rei_dic


def _com_value(commit, module_classes):
    icf_dic = dict()
    ecf_dic = dict()
    rei_dic = dict()
    for module_name1 in module_classes:
        icf_value_list = _com_icf_or_ecf(module_classes[module_name1], module_classes[module_name1], commit)
        ecf_value_list = list()
        for module_name2 in module_classes:
            if module_name1 != module_name2:
                ecf_value_list.extend(_com_icf_or_ecf(module_classes[module_name1], module_classes[module_name2], commit))
        icf = float(format(sum(icf_value_list) / len(icf_value_list), '.4f'))
        ecf = float(format(sum(ecf_value_list) / len(ecf_value_list), '.4f'))
        icf_dic[module_name1] = icf
        ecf_dic[module_name1] = ecf
        rei_dic[module_name1] = float(format(_com_rei(icf, ecf), '.4f'))
    return icf_dic, ecf_dic, rei_dic


def _com_rei(icf, ecf):
    if icf == 0:
        return 0
    return ecf / icf


def _com_icf_or_ecf(current_classes, another_classes, commit):
    res_list = list()
    if len(current_classes) == 0 and len(another_classes) == 0:
        res_list.append(-1)
    if len(another_classes) == 0:
        res_list.append(0)
        return res_list
    for class1 in current_classes:
        for class2 in another_classes:
            res = 0
            if class1 in commit and class2 in commit[class1]:
                res = 1
            res_list.append(res)
    return res_list
