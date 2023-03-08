import pandas as pd
from evaluator.utils import modifier, common
# from evaluator.serializers import MethodDataSerializer


def del_method_dep(call, called, contain, override, overrided, parameter, method_define_var, id, NOP, CTM, RFC, NOSI,
                   method_class, c, variables,
                   method_dic, invoke_local_methods, c_var):
    parm_num = 0
    var_num = 0
    if id in parameter:
        parm_num = len(parameter[id])
    if id in method_define_var:
        c_var.extend(list(method_define_var[id]))
        var_num = len(method_define_var[id])
    # call/override
    IDMC = list()
    EDMC = list()
    FAN_IN = list()
    FAN_OUT = list()
    IsOverride = False
    Overrided = list()
    # All direct invocations of methods
    methodsInvokedQty = 0
    # All direct invocations of methods of the same class
    methodsInvokedLocalQty = 0
    # All indirect invocations of methods of the same class
    methodsInvokedIndirectLocalQty = 0
    invoke_local = list()

    if id in call:
        # deal invoked
        for call_id in call[id]:
            _append_FAN_IN_or_OUT(call_id, method_class, FAN_OUT, c)
            RFC.append(call_id)
            methodsInvokedQty += 1
            if call_id not in method_class or method_class[call_id] != c:
                CTM.append(call_id)
                if 'modifiers' in variables[call_id] and 'static' in variables[call_id]['modifiers']:
                    NOSI.append(call_id)
            else:
                methodsInvokedLocalQty += 1
                invoke_local.append(call_id)

            # methodsInvokedIndirectLocalQty = len(indirect_local_invoke)
            _append_IDMC_or_EDMC(call_id, method_class, contain, EDMC, IDMC, c)
        if id not in invoke_local_methods:
            invoke_local_methods[id] = invoke_local
    # invoked others
    if id in called:
        for called_id in called[id]:
            _append_FAN_IN_or_OUT(called_id, method_class, FAN_IN, c)
            _append_IDMC_or_EDMC(called_id, method_class, contain, EDMC, IDMC, c)
    # override
    if id in override:
        IsOverride = True
        NOP += 1
        _append_FAN_IN_or_OUT(id, method_class, FAN_OUT, c)
        _append_IDMC_or_EDMC(override[id], method_class, contain, EDMC, IDMC, c)
    # overrided
    if id in overrided:
        for methods_id in overrided[id]:
            if methods_id not in method_class:
                continue
            Overrided.append(method_class[methods_id])
            _append_FAN_IN_or_OUT(methods_id, method_class, FAN_IN, c)
            _append_IDMC_or_EDMC(methods_id, method_class, contain, EDMC, IDMC, c)
    method_value = [variables[id]['location']['startLine'],
                    len(set(FAN_IN)) + len(set(FAN_OUT)),
                    len(set(FAN_IN)),
                    len(set(FAN_OUT)),
                    len(set(IDMC)),
                    len(set(EDMC)),
                    IsOverride,
                    len(set(Overrided)),
                    methodsInvokedQty,
                    methodsInvokedLocalQty,
                    methodsInvokedIndirectLocalQty,
                    var_num,
                    parm_num,
                    modifier.get_modifiers(variables[id])]

    # method_df = pd.DataFrame(data={
    #     'metric': common.METHOD_METRICS,
    #     'value': method_value
    # }, columns=['metric', 'value'])
    # method_df['method'] = variables[id]['qualifiedName']
    # method_dic_list = method_df.to_dict(orient='records')
    # for dic in method_dic_list:
    #     dic['classname'] = class_ids
    #
    # # 将方法度量结果入库
    # for data in method_dic_list:
    #     serializer = MethodDataSerializer(data=data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    method_metric = dict(zip(common.METHOD_METRICS, method_value))
    method_dic[variables[id]['qualifiedName']] = method_metric
    return NOP


def _append_IDMC_or_EDMC(id_val, method_class, contain, EDMC, IDMC, current_class):
    if id_val in method_class and method_class[id_val] != current_class:
        if method_class[id_val] not in contain:
            EDMC.append(method_class[id_val])
        else:
            IDMC.append(method_class[id_val])


def _append_FAN_IN_or_OUT(id_val, method_class, lis, current_class):
    if id_val in method_class and method_class[id_val] != current_class:
        lis.append(method_class[id_val])


def _del_overrided(overrided_methods, method_class, contain, EDMC, IDMC):
    for methods_id in overrided_methods:
        if method_class[methods_id] not in contain:
            EDMC += 1
        else:
            IDMC += 1
    return EDMC, IDMC
