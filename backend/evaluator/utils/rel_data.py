from evaluator.utils.json_operator import write_result_to_json


def get_rel_info(json_dic, mapping_dic, result_path):
    cells = json_dic['cells']
    variables = json_dic['variables']

    package_contain = dict()
    class_contain = dict()
    method_define_var = dict()
    method_use_field = dict()
    package_name_to_id = dict()
    file_contain = dict()
    set_var = dict()
    inherit = dict()
    descendent = dict()
    override = dict()
    parameter = dict()
    overrided = dict()
    dep = dict()
    call = dict()
    called = dict()
    import_val = dict()
    imported_val = dict()
    method_class = dict()
    for c in cells:
        # Define
        if 'Define' in c['values']:
            if variables[c['src']]['category'] == 'Class':
                if c['src'] not in class_contain:
                    class_contain[c['src']] = list()
                class_contain[c['src']].append(c['dest'])
                if variables[c['dest']]['category'] == 'Method':
                    method_class[c['dest']] = c['src']
            if variables[c['src']]['category'] == 'Method' and variables[c['dest']]['category'] == 'Variable':
                if c['src'] not in method_define_var:
                    method_define_var[c['src']] = set(list())
                method_define_var[c['src']].add(c['dest'])
        # Set
        if 'Set' in c['values']:
            if c['src'] not in set_var:
                set_var[c['src']] = list()
            set_var[c['src']].append(c['dest'])
        # Contain
        if 'Contain' in c['values']:
            if variables[c['src']]['category'] == 'Package' and variables[c['dest']]['category'] == 'File':
                if c['src'] not in package_contain:
                    package_contain[c['src']] = list()
                package_contain[c['src']].append(c['dest'])
                package_name_to_id[variables[c['src']]['qualifiedName']] = c['src']
            if variables[c['src']]['category'] == 'File' and variables[c['dest']]['category'] == 'Class':
                file_contain[c['src']] = c['dest']
        if variables[c['src']]['category'] == 'Method' and variables[c['dest']]['category'] == 'Variable':
            # UseVar
            if 'UseVar' in c['values']:
                if c['src'] not in method_use_field:
                    method_use_field[c['src']] = set(list())
                if variables[c['dest']]['global']:
                    method_use_field[c['src']].add(c['dest'])
            # Parameter
            if 'Parameter' in c['values']:
                if c['src'] not in parameter:
                    parameter[c['src']] = list()
                parameter[c['src']].append(c['dest'])
        # Inherit/Import/Implement/Cast/Reflect/Annotate
        if 'Inherit' in c['values'] or 'Import' in c['values'] or 'Implement' in c['values']:
            if 'Inherit' in c['values']:
                _add_list_value(inherit, c['src'], c['dest'])
                _add_list_value(descendent, c['dest'], c['src'])
            if 'Import' in c['values']:
                _add_list_value(import_val, c['src'], c['dest'])
                _add_list_value(imported_val, c['dest'], c['src'])
            _add_dep(dep, c['src'], c['dest'])
        if 'Call' in c['values']:
            _add_list_value(call, c['src'], c['dest'])
            _add_list_value(called, c['dest'], c['src'])
        # Call non-dynamic/Override (they have included in inherit, so don't need to be added in dep)
        if 'Call non-dynamic' in c['values'] or 'Override' in c['values']:
            override[c['src']] = c['dest']
            _add_list_value(overrided, c['dest'], c['src'])

    # call -> dep
    _convert_call_to_dep(call, method_class, dep)
    # moduleinfo: class -> field/method
    module_info = _get_module_info(mapping_dic, package_contain, package_name_to_id, file_contain, class_contain,
                                   method_use_field, set_var, variables)
    # save call/called/inherit/descendent/import_val/imported_val into a dep file
    _save_dep_to_json(inherit, descendent, call, called, import_val, imported_val, parameter,
                      variables, result_path)

    return module_info, method_class, call, called, dep, inherit, descendent, override, overrided, import_val, imported_val, parameter, method_define_var, method_use_field


def _save_dep_to_json(inherit, descendent, call_id_dic, called_id_dic, import_val, imported_val,
                      parameter, variables, result_path):
    result = dict()
    result['inherit'] = _convert_dep_name_dic(inherit, variables)
    result['descendent'] = _convert_dep_name_dic(descendent, variables)
    result['import'] = _convert_dep_name_dic(import_val, variables)
    result['imported'] = _convert_dep_name_dic(imported_val, variables)
    result['call'] = _convert_call_method_name_dic(call_id_dic, parameter, variables)
    result['called'] = _convert_call_method_name_dic(called_id_dic, parameter, variables)
    write_result_to_json(result_path + '/dep.json', result)


def _convert_dep_name_dic(id_dic, variables):
    result = dict()
    for src_id in id_dic:
        if variables[src_id]['qualifiedName'] not in result:
            result[variables[src_id]['qualifiedName']] = list()
        for dest_id in id_dic[src_id]:
            result[variables[src_id]['qualifiedName']].append(variables[dest_id]['qualifiedName'])
    return result


def _convert_call_method_name_dic(id_dic, parameter, variables):
    name_dic = dict()
    for method_id1 in id_dic:
        method_name1 = _get_method_name(method_id1, parameter, variables)
        if method_name1 not in name_dic:
            name_dic[method_name1] = list()
        for method_id2 in id_dic[method_id1]:
            name_dic[method_name1].append(_get_method_name(method_id2, parameter, variables))
    return name_dic


def _get_method_name(method_id, parameter, variables):
    if method_id not in parameter:
        return variables[method_id]['qualifiedName'] + '/0'
    return variables[method_id]['qualifiedName'] + '/' + str(len(parameter[method_id]))


def _add_dep(dic, src_id, dest_id):
    if src_id not in dic:
        dic[src_id] = dict()
    if dest_id not in dic[src_id]:
        dic[src_id][dest_id] = 0
    dic[src_id][dest_id] += 1


def _add_list_value(dic, id1, id2):
    if id1 not in dic:
        dic[id1] = list()
    dic[id1].append(id2)


def _convert_call_to_dep(call, method_class, dep):
    for src_method_id in call:
        for dest_method_id in call[src_method_id]:
            if src_method_id in method_class and dest_method_id in method_class:
                if method_class[src_method_id] not in dep:
                    dep[method_class[src_method_id]] = dict()
                if method_class[dest_method_id] not in dep[method_class[src_method_id]]:
                    dep[method_class[src_method_id]][method_class[dest_method_id]] = 0
                dep[method_class[src_method_id]][method_class[dest_method_id]] += 1


def _get_module_info(mapping_dic, package_contain, package_name_to_id, file_contain, class_contain, method_use_field,
                     set_var, variables):
    module_info = dict()
    if mapping_dic:
        for module in mapping_dic:
            packages = mapping_dic[module]
            module_info[module] = dict()
            for package in packages:
                for file in package_contain[package_name_to_id[package]]:
                    if file in file_contain and file_contain[file] in class_contain:
                        module_info[module][file_contain[file]] = class_contain[file_contain[file]]
                if len(module_info[module]) == 0:
                    del module_info[module]
    else:
        for package in package_contain:
            module_info[package] = dict()
            for file in package_contain[package]:
                if file in file_contain and file_contain[file] in class_contain:
                    contain_list = list()
                    for method_or_field_id in class_contain[file_contain[file]]:
                        contain_list.append(method_or_field_id)
                        if variables[method_or_field_id][
                            'category'] == 'Method' and method_or_field_id in method_use_field:
                            contain_list.extend(method_use_field[method_or_field_id])
                    if file_contain[file] in set_var:
                        contain_list.extend(set_var[file_contain[file]])
                    module_info[package][file_contain[file]] = list(set(contain_list))
            if len(module_info[package]) == 0:
                del module_info[package]
    return module_info
