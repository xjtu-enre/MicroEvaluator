import pandas as pd
import numpy as np
from evaluator.generalevaluator.object_oriented_measurement.class_metric_compete import class_and_method_metric_compete
from evaluator.generalevaluator.module_measurement.compete_strcut_dep import com_struct_metric
from evaluator.generalevaluator.module_measurement.moduarity.sf_measure import get_spread_and_focus
from evaluator.generalevaluator.module_measurement.evolution.com_icf_ecf import get_icf_ecf_rei
from evaluator.utils import common
from evaluator.serializers import *
from evaluator.utils.index_measure import get_score


def get_module_metric(variables, package_info, inherit, descendent, method_class, struct_dep, call, called, override,
                      overrided, import_val, imported_val, parameter, method_define_var, method_use_field, cmt_path,
                      type, version_id, module_data):
    # measure history dep
    focus_dic, spread_dic, module_classes, commit = get_spread_and_focus(cmt_path, package_info, variables)
    icf_dic, ecf_dic, rei_dic = get_icf_ecf_rei(module_classes, commit)
    # measure structure dep
    module_dic = dict()
    module_list = list()
    for package in package_info:
        if type == 'module':
            package_name = package
        else:
            package_name = variables[package]['qualifiedName']
        module_value, idcc_list, edcc_list, fan_in, fan_out, iodd, iidd = com_struct_metric(package, package_info,
                                                                                            struct_dep)

        module_value.extend(
            [spread_dic[package_name], focus_dic[package_name], icf_dic[package_name], ecf_dic[package_name],
             rei_dic[package_name], len(package_info[package])])
        module_data.append(module_value[0:])
        module_df = pd.DataFrame(data={
            'metric': common.MODULE_METRICS,
            'value': module_value
        }, columns=['metric', 'value'])
        module_df['module'] = package_name
        module_df['version'] = version_id

        # # 将模块度量结果入库
        module_ids = list()
        # # serializer = ModuleDataSerializer(data=module_df.to_dict(orient='records'), many=True)
        # for data in module_df.to_dict(orient='records'):
        #     serializer = ModuleDataSerializer(data=data)
        #     if serializer.is_valid(raise_exception=True):
        #         serializer.save()
        #     module_ids.append(serializer.data['id'])
        class_dic = class_and_method_metric_compete(variables, package_info[package], inherit, descendent, parameter,
                                                       method_define_var, method_use_field, method_class, call, called,
                                                       idcc_list, edcc_list, override, overrided, import_val,
                                                       imported_val,
                                                       fan_in, fan_out, iodd, iidd, module_ids)
        print('end to compete metrics!')
        module_metric = dict(zip(common.MODULE_METRICS, module_value))
        module_metric['classes'] = class_dic
        module_dic[package_name] = module_metric
        module_list.append([module_metric['scoh'], module_metric['scop'],
                            module_metric['odd'], module_metric['idd']])
    [normalized_result, score_result] = get_score(module_list,
                                                  [[0.25], [0.25], [0.25], [0.25]],
                                                  ['scoh', 'scop', 'odd', 'idd'])

    return module_dic, np.mean(score_result)
