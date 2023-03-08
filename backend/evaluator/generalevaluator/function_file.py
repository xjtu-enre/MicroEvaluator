from evaluator.generalevaluator.module_measurement.module_metric_compete import get_module_metric
from evaluator.generalevaluator.analysis.indicate import gen_xlsx
from evaluator.utils.rel_data import *
from evaluator.utils.csv_operator import *
from evaluator.utils.json_operator import *
from evaluator.utils.db_operator import *
from evaluator.utils.common import *
from operator import itemgetter
from project.models import *


def measure_module_metrics(dep_path, cmt_path, mapping_path):
    dep_dic = read_file(dep_path)
    mapping_dic = read_file(mapping_path)
    if dep_dic and mapping_dic:
        module_info, method_class, call, called, dep, inherit, descendent, override, overrided, import_val, imported_val, parameter, method_define_var, method_use_field = get_rel_info(
            dep_dic, mapping_dic)
        module_dic = get_module_metric(dep_dic['variables'], module_info, inherit, descendent, method_class, dep, call,
                                       called, override, overrided, import_val, imported_val, parameter,
                                       method_define_var, method_use_field,
                                       cmt_path, 'module')
        write_result_to_json('measure_result.json', module_dic)
        write_result_to_csv('measure_result_class.csv', 'measure_result_method.csv', module_dic)
        return True
    return False


def measure_package_metrics(dep_path, cmt_path, result_path, version_id, version, project_dic, project_name):
    dep_dic = read_file(dep_path)
    if dep_dic:
        module_data = list()
        # 获取依赖信息
        package_info, method_class, call, called, dep, inherit, descendent, override, overrided, import_val, imported_val, parameter, method_define_var, method_use_field = get_rel_info(
            dep_dic, dict(), result_path)
        # 基于依赖信息进行度量
        module_dic, score = get_module_metric(dep_dic['variables'], package_info, inherit, descendent, method_class, dep,
                                        call, called, override, overrided, import_val, imported_val, parameter,
                                        method_define_var,
                                        method_use_field, cmt_path, 'package', version_id, module_data)
        result = list()
        for item in module_data:
            temp = [item[0] - item[1]]
            temp.extend(item[2: 11: 1])
            result.append(temp)
        tmp_pro = np.around(np.array(result).mean(axis=0).tolist(), 4)
        project_dic = dict()
        tmp_pro = np.insert(tmp_pro, 0, score)
        project_metric = dict(zip(PROJECT_METRICS, tmp_pro))
        project_metric['modules'] = module_dic
        project_dic[version] = project_metric
        ver = VersionProject.objects.filter(id=version_id).first().version
        write_result_to_json('./featureextractor/data/' + project_name + '/' + ver + '/measure_result.json', project_dic)
        # 项目级数据入库
        save_project_to_db(module_data, version_id, module_dic, project_dic)


def compare_diff(folder_path1, folder_path2, mapping, output):
    measure_json_dict1, dep_json_dict1 = read_folder(folder_path1, 'measure_result.json', 'dep.json')
    measure_json_dict2, dep_json_dict2 = read_folder(folder_path2, 'measure_result.json', 'dep.json')
    if mapping:
        pp_mapping = read_file(mapping)
        # convert result1's packages' old name to new name
        _convert_old_to_new(measure_json_dict1, pp_mapping)
    if not (measure_json_dict1 or measure_json_dict2 or dep_json_dict1 or dep_json_dict2):
        return False
    # if not (measure_list[1] or measure_list[0] or dep_list[1] or dep_list[0]):
    #     return dict()
    measure_diff = dict()
    dep_diff = dict()
    metric_change = list()
    modules_name = list()
    _get_measure_diff(measure_json_dict1, measure_json_dict2, measure_diff, modules_name, metric_change)
    _get_dep_diff(dep_json_dict1, dep_json_dict2, dep_diff)
    write_result_to_json(create_file_path(output + '\\diffResult', 'measure_diff.json'), measure_diff)
    write_result_to_json(create_file_path(output + '\\diffResult', 'dep_diff.json'), dep_diff)
    gen_xlsx(create_file_path(output + '\\diffResult', 'diff_result.xlsx'), metric_change, modules_name, measure_diff)
    return measure_diff


def _get_measure_diff(measure_json_dict1, measure_json_dict2, measure_diff, modules_name, metric_change):
    module2_info = measure_json_dict2
    module1_info = measure_json_dict1
    for module_name in module2_info:
        if module_name in module1_info:
            module_result1 = module1_info[module_name]
            module_result2 = module2_info[module_name]
            module_value1 = list(itemgetter(*MODULE_METRICS)(module_result1))
            module_value2 = list(itemgetter(*MODULE_METRICS)(module_result2))
            module_diff_value = _diff_value(module_value1, module_value2)
            module_diff_dict = dict(zip(MODULE_METRICS, module_diff_value))
            measure_diff[module_name] = module_diff_dict
            modules_name.append(module_name)
            metric_change.append(module_diff_value)
            classes = dict()
            # 11->12 changed and added classes
            for class_name in module_result2['classes']:
                if class_name in module_result1['classes']:
                    class2 = module_result2['classes'][class_name]
                    class1 = module_result1['classes'][class_name]
                    _diff_classes(classes, class_name, class1, class2)
                    methods = dict()
                    for method_name in class2['methods']:
                        if method_name in class1['methods']:
                            method1_val = class1['methods'][method_name]
                            method2_val = class2['methods'][method_name]
                            _diff_methods(methods, method_name, method1_val, method2_val)
                        else:
                            methods[method_name] = class2['methods'][method_name]
                            methods[method_name]['status'] = 'add'
                    # 11->12 deleted methods
                    for method_name in class1['methods']:
                        if method_name not in class2['methods']:
                            methods[method_name] = class1['methods'][method_name]
                            methods[method_name]['status'] = 'delete'
                    classes[class_name]['methods'] = methods
                else:
                    classes[class_name] = module_result2['classes'][class_name]
                    classes[class_name]['status'] = 'add'
            # 11->12 deleted classes
            for class_name in module_result1['classes']:
                if class_name not in module_result2['classes']:
                    classes[class_name] = module_result1['classes'][class_name]
                    classes[class_name]['status'] = 'delete'

            measure_diff[module_name]['classes'] = classes


def _diff_value(list1, list2):
    res = list()
    for i in range(len(list1)):
        res.append(float(list2[i]) - float(list1[i]))
    return res


def _get_dep_diff(dep_json_dict1, dep_json_dict2, dep_diff):
    dep_diff['inherit'] = _get_diff(dep_json_dict1['inherit'], dep_json_dict2['inherit'])
    dep_diff['descendent'] = _get_diff(dep_json_dict1['descendent'], dep_json_dict2['descendent'])
    dep_diff['call'] = _get_diff(dep_json_dict1['call'], dep_json_dict2['call'])
    dep_diff['called'] = _get_diff(dep_json_dict1['called'], dep_json_dict2['called'])
    dep_diff['import'] = _get_diff(dep_json_dict1['import'], dep_json_dict2['import'])
    dep_diff['imported'] = _get_diff(dep_json_dict1['imported'], dep_json_dict2['imported'])


def _get_diff(dep_dic1, dep_dic2):
    result = dict()
    for dep_src_name in dep_dic2:
        if dep_src_name in dep_dic1:
            # 11->12 add
            for dep_dest_name2 in dep_dic2[dep_src_name]:
                if dep_dest_name2 not in dep_dic1[dep_src_name]:
                    if dep_src_name not in result:
                        result[dep_src_name] = list()
                    result[dep_src_name].append({'name': dep_dest_name2, 'status': 'add dep'})
            # 11->12 delete
            for dep_dest_name1 in dep_dic1[dep_src_name]:
                if dep_dest_name1 not in dep_dic2[dep_src_name]:
                    if dep_src_name not in result:
                        result[dep_src_name] = list()
                    result[dep_src_name].append({'name': dep_dest_name1, 'status': 'delete dep'})
        else:
            dep_dic2[dep_src_name].append('status:new class')
            result[dep_src_name] = dep_dic2[dep_src_name]
    return result


def _convert_old_to_new(old_name_ver_data, mapping):
    new_name_ver_data = dict()
    for module in old_name_ver_data:
        new_name = module
        for old_name in mapping:
            if old_name in module:
                new_name = module.replace(old_name, mapping[old_name])
                break
        new_name_ver_data[new_name] = {'scoh': old_name_ver_data[module]['scoh'],
                                       'scop': old_name_ver_data[module]['scop'],
                                       'idd': old_name_ver_data[module]['idd'],
                                       'odd': old_name_ver_data[module]['odd'],
                                       'DSM': old_name_ver_data[module]['DSM']}
        new_classes = dict()
        for class_name in old_name_ver_data[module]['classes']:
            new_class_name = class_name.replace(module, new_name)
            new_classes[new_class_name] = old_name_ver_data[module]['classes'][class_name]
        new_name_ver_data[new_name]['classes'] = new_classes
    return new_name_ver_data


def _diff_classes(classes, class_name, class1, class2):
    class_value1 = list(itemgetter(*CLASS_METRICS)(class1))
    class_value2 = list(itemgetter(*CLASS_METRICS)(class2))
    class_diff_value = _diff_value(class_value1, class_value2)
    class_diff_dict = dict(zip(CLASS_METRICS, class_diff_value))
    classes[class_name] = class_diff_dict


def _diff_methods(methods, method_name, method1_val, method2_val):
    method_value1 = list(itemgetter(*METHOD_METRICS)(method1_val))
    method_value2 = list(itemgetter(*METHOD_METRICS)(method2_val))
    method_diff_value = _diff_value(method_value1, method_value2)
    method_diff_dict = dict(zip(METHOD_METRICS, method_diff_value))
    methods[method_name] = method_diff_dict


def _get_isOverride(method1_isOveeride_val, method2_isOveeride_val):
    # TRUE -> TRUE
    if method1_isOveeride_val and method2_isOveeride_val:
        return 0
    # FALSE -> FALSE
    if not method1_isOveeride_val and not method2_isOveeride_val:
        return 1
    # TRUE -> FALSE
    if method1_isOveeride_val and not method2_isOveeride_val:
        return 2
    # FALSE -> TRUE
    if not method1_isOveeride_val and method2_isOveeride_val:
        return 3


def create_file_path(folder_path, file_name):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return os.path.join(folder_path, file_name)