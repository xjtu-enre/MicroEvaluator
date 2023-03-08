from evaluator.generalevaluator.object_oriented_measurement.method_metric_compete import del_method_dep
from evaluator.utils.modifier import get_modifiers, judge_modifier_type
from evaluator.generalevaluator.object_oriented_measurement.cohesion.com_functionality import com_chm, com_chd
from evaluator.utils.common import *
from evaluator.serializers import *
import pandas as pd


def class_and_method_metric_compete(variables, contain, inherit, descendent, parameter, method_define_var,
                                    method_use_field, method_class, call, called, idcc_list,
                                    edcc_list, override, overrided, import_val, imported_val,
                                    fan_in, fan_out, iodd, iidd, module_ids):
    print('begin to compete class-level metrics!')
    class_dic = dict()
    for c in contain:
        # 先将class的一些信息入一次库，后面再更新，主要是为了取id给method入库使用
        # class_df = pd.DataFrame(data={
        #     'metric': CLASS_METRICS,
        # }, columns=['metric'])
        # class_df['classname'] = variables[c]['qualifiedName']
        # class_dic_list = class_df.to_dict(orient='records')
        # for dic in class_dic_list:
        #     dic['module'] = module_ids
        #
        # # 将类度量结果入库
        # class_ids = list()
        # for data in class_dic_list:
        #     serializer = ClassDataSerializer(data=data)
        #     if serializer.is_valid(raise_exception=True):
        #         serializer.save()
        #         class_ids.append(serializer.data['id'])

        print('current class:', c)
        dic_id = contain[c]
        cis = 0
        # ctm/nosi: invoke how many (static) methods
        ctm = list()
        rfc = list()
        nosi = list()
        nop = 0
        private_var_num = 0
        public_var_num = 0
        protected_var_num = 0
        static_var_num = 0
        default_var_num = 0
        final_var_num = 0
        synchronized_var_num = 0
        private_methods_num = 0
        protected_methods_num = 0
        static_methods_num = 0
        default_methods_num = 0
        abstract_methods_num = 0
        final_methods_num = 0
        synchronized_methods_num = 0
        method_dic = dict()
        # c_var contains fields
        c_var = list()
        fields = list()
        methods_id = list()
        visible_methods_id = list()
        current_method_use_field = dict()
        invoke_local_methods = dict()
        for id in dic_id:
            # if 'modifiers' in variables[id]:
            if variables[id]['category'] == 'Method':
                methods_id.append(id)
                if id in method_use_field:
                    current_method_use_field[id] = method_use_field[id]
                # different methods num
                cis, protected_methods_num, private_methods_num, static_methods_num, default_methods_num, final_methods_num, synchronized_methods_num, abstract_methods_num = judge_modifier_type(
                    variables[id], cis, protected_methods_num, private_methods_num, static_methods_num,
                    default_methods_num, final_methods_num, synchronized_methods_num, abstract_methods_num)
                # default
                if 'modifiers' not in variables[id]:
                    visible_methods_id.append(id)
                # not private
                elif 'private' not in variables[id]['modifiers']:
                    visible_methods_id.append(id)
                # dep of method(call/override)
                nop = del_method_dep(call, called, contain, override,
                                     overrided,
                                     parameter, method_define_var, id,
                                     nop, ctm, rfc, nosi,
                                     method_class, c, variables,
                                     method_dic, invoke_local_methods, c_var)
            elif variables[id]['category'] == 'Variable':
                c_var.append(id)
                fields.append(id)
                # different variables num
                public_var_num, protected_var_num, private_var_num, static_var_num, default_var_num, final_var_num, synchronized_var_num, abstrcat_num = judge_modifier_type(
                    variables[id], public_var_num, protected_var_num, private_var_num, static_var_num, default_var_num,
                    final_var_num, synchronized_var_num, 0)

        # deal indirect invoke(call tree in the class)
        # method_invocations_indirect_local = _get_invoke_indirect_local(methods_id, invoke_local_methods)
        # get info of visible methods
        # _get_all_accessed_fields(visible_methods_id, all_accessed_fields, method_use_field,
        #                           method_invocations_indirect_local)
        # direct_connections, indirect_connections = _get_methods_conn(all_accessed_fields, visible_methods_id)
        # tcc = _com_tcc_or_lcc(direct_connections, list(), len(visible_methods_id))
        # lcc = _com_tcc_or_lcc(direct_connections, indirect_connections, len(visible_methods_id))
        nac = find_node_num(inherit, c, variables, 1)
        ndc = find_node_num(descendent, c, variables, 0)
        # lcom = _com_lcom(methods_id, current_method_use_field)
        # locm_normalized = _com_locm_normalized(len(methods_id), fields, current_method_use_field)
        c_chm = com_chm(methods_id, parameter, variables)
        c_chd = com_chd(methods_id, parameter, variables)
        class_value = [cis, len(methods_id), nop, nac, ndc, _get_number_of_import(import_val, c),
                       _get_number_of_import(imported_val, c), len(set(ctm)), idcc_list[c], iodd[c], iidd[c],
                       edcc_list[c], fan_in[c], fan_out[c], fan_in[c] + fan_out[c], format(c_chm, '.4f'),
                       format(c_chd, '.4f'), len(set(c_var)),
                       private_methods_num, protected_methods_num, static_methods_num, default_methods_num,
                       abstract_methods_num, final_methods_num, synchronized_methods_num,
                       public_var_num, private_var_num, protected_var_num, static_var_num, default_var_num,
                       final_var_num,
                       synchronized_var_num, len(set(rfc)),
                       len(fields), len(visible_methods_id), len(set(nosi)), 0, 0, 0, 0, len(methods_id),
                       get_modifiers(variables[c])]

        # # 更新这个class中的value信息
        # index = 0
        # for class_id in class_ids:
        #     ClassData.objects.filter(id=class_id).update(value=class_value[index])
        #     index += 1

        class_metric = dict(zip(CLASS_METRICS, class_value))
        class_metric['methods'] = method_dic
        class_dic[variables[c]['qualifiedName']] = class_metric
    return class_dic

def _get_invoke_indirect_local(methods_id, invoke_local_methods):
    method_invocations_indirect_local = dict()

    for method_id in methods_id:
        local_invocations = _invocation(method_id, dict(), invoke_local_methods)
        method_invocations_indirect_local[method_id] = local_invocations
    return method_invocations_indirect_local


def _invocation(method_id, explored, invoke_local_methods):
    if method_id not in invoke_local_methods:
        return explored

    next_invocations = list()
    for called_id in invoke_local_methods[method_id]:
        if called_id not in explored and method_id != called_id:
            next_invocations.append(called_id)
    if len(next_invocations) > 0:
        explored[method_id] = next_invocations
        for next_invocation in next_invocations:
            _invocation(next_invocation, explored, invoke_local_methods)
    return explored


def _get_number_of_import(dic, c):
    if c in dic:
        return len(dic[c])
    return 0


def _get_all_accessed_fields(visible_methods_id, all_accessed_fields, method_use_field,
                             method_invocations_indirect_local):
    all_local_fields = list()
    for method_id in visible_methods_id:
        if method_id in method_use_field:
            all_local_fields.extend(method_use_field[method_id])
        _collect_accessed_fields(method_id, method_use_field, all_local_fields, method_invocations_indirect_local)
        all_accessed_fields[method_id] = set(all_local_fields)


def _get_methods_conn(all_accessed_fields, visible_methods_id):
    # Two methods are directly connected if:
    # 1. both access the same class-level variable
    # 2. their call trees access the same class-level variable (only within the class)
    direct_connections = list()
    for first_key in all_accessed_fields:
        for second_key in all_accessed_fields:
            # len(all_accessed_fields) == len(visible_methods_id)
            intersec = all_accessed_fields[first_key].intersection(all_accessed_fields[second_key])
            if first_key != second_key and len(intersec) > 0:
                direct_connections.append([first_key, second_key])
    # Two methods are indirectly connected if:
    # 1. they are not directly connected
    # 2. they are connected via other methods, e.g. X -> Y -> Z
    indirect_connections = list()
    _get_indirect_connections(visible_methods_id, direct_connections, indirect_connections)

    return direct_connections, indirect_connections


def _com_tcc_or_lcc(direct_connections, indirect_connections, novm):
    if novm == 0:
        return -1
    elif novm == 1:
        return 1
    else:
        return (len(direct_connections) + len(indirect_connections)) / float(novm * (novm - 1))


def _com_locm_normalized(methods_num, fields, current_method_use_field):
    lcom_normalized = 0
    sum = 0
    if methods_num != 0:
        for field_id in fields:
            field_in_method_num = _get_field_in_method_num(field_id, current_method_use_field)
            sum += (methods_num - field_in_method_num) / methods_num

        if len(fields) > 0:
            lcom_normalized = (1 * sum) / len(fields)
    return lcom_normalized


def _get_field_in_method_num(field_id, current_method_use_field):
    num = 0
    for method_id in current_method_use_field:
        if field_id in current_method_use_field[method_id]:
            num += 1
    return num


def _collect_accessed_fields(method_id, method_use_field, all_local_fields, method_invocations_indirect_local):
    all_local_invocations = list(method_invocations_indirect_local[method_id].keys())

    for local_invocation_id in all_local_invocations:
        if local_invocation_id in method_use_field:
            current_fields = method_use_field[local_invocation_id]
            if current_fields:
                all_local_fields.extend(list(current_fields))


def _com_lcom(methods_id, current_method_use_field):
    lcom = 0
    for index1 in range(0, len(methods_id)):
        for index2 in range(index1 + 1, len(methods_id)):
            intersection_fields = list()
            if methods_id[index1] in current_method_use_field and methods_id[index2] in current_method_use_field:
                intersection_fields = list(current_method_use_field[methods_id[index1]].intersection(
                    current_method_use_field[methods_id[index2]]))
            if len(intersection_fields) == 0:
                lcom += 1
            else:
                lcom -= 1
    return lcom if lcom > 0 else 0


def _get_indirect_connections(visible_methods_id, direct_connections, indirect_connections):
    direct_connections_map = dict()
    for index in range(0, len(direct_connections)):
        if direct_connections[index][0] not in direct_connections_map:
            direct_connections_map[direct_connections[index][0]] = list()
        direct_connections_map[direct_connections[index][0]].append(direct_connections[index][1])

    # extract all direct and indirect connections between methods from the direct connections(nodes in this call tree)
    indirect_connections_map = dict()
    for method_id in visible_methods_id:
        local_connections = extract_connections(method_id, set(), direct_connections_map)
        indirect_connections_map[method_id] = local_connections

    # map the indirect connections into connection pairs
    temp_indirect_connections = list()
    for method_id in indirect_connections_map:
        for right_method_id in indirect_connections_map[method_id]:
            if method_id != right_method_id:
                temp_indirect_connections.append([method_id, right_method_id])

    # remove all direct connections
    for temp in temp_indirect_connections:
        flag = False
        for dir_conn in direct_connections:
            if temp[0] == dir_conn[0] and temp[1] == dir_conn[1]:
                flag = True
                break
        if not flag:
            indirect_connections.append(temp)


def extract_connections(method_id, explored, direct_connections_map):
    explored.add(method_id)
    next_connections = set()
    if method_id in direct_connections_map:
        for connection in direct_connections_map[method_id]:
            if connection not in explored:
                next_connections.add(connection)
                explored.add(connection)

        for next_connection in next_connections:
            explored = explored | extract_connections(next_connection, explored, direct_connections_map)
    return explored


def find_node_num(rel_dic, class_id, variables, count):
    if class_id in rel_dic:
        count += len(rel_dic[class_id])
        for parent_id in rel_dic[class_id]:
            find_node_num(rel_dic, parent_id, variables, count)
    return count

#
# if __name__ == '__main__':
#     test = set()
#     test.add((1, 2,3))
#     test.add((4, 5,6))
#
#     print(test)
