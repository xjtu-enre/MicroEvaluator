import csv

from rest_framework import viewsets
from rest_framework import permissions
from evaluator.models import *
from evaluator.serializers import *
from evaluator.utils.common import *
from evaluator.utils.datautil import *
from evaluator.generalevaluator.detect_algo.detect_root_cause import *
# from rest_framework.status import HTTP_200_OK
# from backend.utils.response import APIResponse
from django.http import JsonResponse
from evaluator.utils.datautil import get_level
import json
import numpy


# class ProjectDataViewSet(viewsets.ModelViewSet):
#     queryset = ProjectData.objects.all()
#     serializer_class = ProjectDataSerializer
#
#     # 需要取项目级和模块级所有指标结果
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         result = list()
#         result.append(serializer.data)
#         result.append([{opt1: 'project', opt2: PROJECT_METRICS}, {opt1: 'module', opt2: MODULE_METRICS}])
#         return APIResponse(HTTP_200_OK, 'list success', serializer.data)
#
#
# class ModuleDataViewSet(viewsets.ModelViewSet):
#     queryset = ModuleData.objects.all()
#     serializer_class = ModuleDataSerializer
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         return APIResponse(HTTP_200_OK, 'list success', serializer.data)

# TODO:暂时用表处理，后期数据库优化后用数据库
def get_all_metric_data(request):
    result = dict()
    # json_list = load_json()
    # get_project_data(json_list)
    module_metrics = list()
    module_metrics.append('score')
    # module_metrics.extend(TEMP_MODULE_METRICS)
    result['scatterdata'], result['projectname'] = get_scatter_data()
    # result['metrics'] = [{'opt1': 'module', 'opt2': module_metrics}]
    result['metrics'] = [{'opt1': 'project', 'opt2': module_metrics}]
    json_str = json.dumps(result, ensure_ascii=False)
    return JsonResponse(json_str, safe=False)


def get_line_data(request):
    result = dict()
    module_metrics = list()
    module_metrics.append('score')
    result['linedata'] = np.array(
        pd.read_csv(r'E:\度量\tools\MicroEvaluator-main\backend\evaluator/linedata.csv', header=None)).tolist()

    json_str = json.dumps(result, ensure_ascii=False)
    return JsonResponse(json_str, safe=False)


def get_metric_data(request):
    result = dict()
    metricdata = pd.read_json(r"E:\度量\tools\MicroEvaluator-main\backend\evaluator/metricdata.json", encoding="utf-8",
                              orient='records')
    # metricdata = pd.read_csv(r'E:\MicroEvaluator\backend\evaluator/metricdata.csv', header=None)
    metricdata = metricdata[list(metricdata.keys())[0]]
    modules, columndata1, columndata2, columndata3 = get_column_data(metricdata)
    result['modularity'] = dict()
    radardata1 = dict()
    radardata1['radarValue'] = [metricdata['SMQ'], metricdata['ODD'], metricdata['IDD']]
    radardata1['indicator'] = ['SMQ', 'ODD', 'IDD']
    result['modularity']['radardata'] = radardata1
    result['modularity']['columndata'] = columndata1
    result['modularity']['modules'] = modules

    result['evolutionary'] = dict()
    radardata2 = dict()
    radardata2['radarValue'] = [metricdata['ICF'], metricdata['ECF'], metricdata.loc['ECF'], metricdata.loc['SPREAD'],
                                metricdata.loc['FOUCUS']]
    radardata2['indicator'] = ['ICF', 'ECF', 'REI', 'SPREAD', 'FOCUS']
    result['evolutionary']['radardata'] = radardata2
    result['evolutionary']['columndata'] = columndata2
    result['evolutionary']['modules'] = modules

    result['functionality'] = dict()
    radardata3 = dict()
    radardata3['radarValue'] = [metricdata['CHM'], metricdata['CHD']]
    radardata3['indicator'] = ['CHM', 'CHD']
    result['functionality']['radardata'] = radardata3
    result['functionality']['columndata'] = columndata3
    result['functionality']['modules'] = modules

    json_str = json.dumps(result, ensure_ascii=False)
    return JsonResponse(json_str, safe=False)


def get_column_data(metricdata):
    modules = list()
    columndata1 = dict()
    columndata1['indicator'] = ['scoh', 'scop', 'odd', 'idd']

    columndata2 = dict()
    columndata2['indicator'] = ['icf', 'ecf', 'rei', 'spread', 'focus']

    columndata3 = dict()
    columndata3['indicator'] = ['chm', 'chd']

    scoh_list = list()
    scop_list = list()
    odd_list = list()
    idd_list = list()
    icf_list = list()
    ecf_list = list()
    rei_list = list()
    spread_list = list()
    focus_list = list()
    chm_list = list()
    chd_list = list()
    for modu in metricdata['modules']:
        modules.append(modu)
        scoh_list.append(metricdata['modules'][modu]['scoh'])
        scop_list.append(metricdata['modules'][modu]['scop'])
        odd_list.append(metricdata['modules'][modu]['odd'])
        idd_list.append(metricdata['modules'][modu]['idd'])
        icf_list.append(metricdata['modules'][modu]['icf'])
        ecf_list.append(metricdata['modules'][modu]['ecf'])
        rei_list.append(metricdata['modules'][modu]['rei'])
        spread_list.append(metricdata['modules'][modu]['spread'])
        focus_list.append(metricdata['modules'][modu]['focus'])
        chm_list.append(metricdata['modules'][modu]['chm'])
        chd_list.append(metricdata['modules'][modu]['chd'])
    columndata1['columnValue'] = [scoh_list, scop_list, odd_list, idd_list]
    columndata2['columnValue'] = [icf_list, ecf_list, rei_list, spread_list, focus_list]
    columndata3['columnValue'] = [chm_list, chd_list]
    return modules, columndata1, columndata2, columndata3


def get_tree_data(request):
    result = dict()
    metricdata = pd.read_json(r"E:\度量\tools\MicroEvaluator-main\backend\evaluator/metrictree.json", encoding="utf-8",
                              orient='records')
    metricdata = metricdata[list(metricdata.keys())[0]]
    module_data = metricdata['modules']
    res = list()
    id = 0
    for index in range(0, 3):
        modu = list(module_data.keys())[index]
        tmp_module = list()
        id += 1
        tmp_module.append({'id': id, 'label': 'scoh:' + str(module_data[modu]['scoh']), 'level': 2})
        id += 1
        tmp_module.append({'id': id, 'label': 'scop:' + str(module_data[modu]['scop']), 'level': 2})
        id += 1
        tmp_module.append({'id': id, 'label': 'odd:' + str(module_data[modu]['odd']), 'level': 2})
        id += 1
        tmp_module.append({'id': id, 'label': 'idd:' + str(module_data[modu]['idd']), 'level': 2})
        id += 1
        tmp_module.append({'id': id, 'label': 'spread:' + str(module_data[modu]['spread']), 'level': 2})
        id += 1
        tmp_module.append({'id': id, 'label': 'focus:' + str(module_data[modu]['focus']), 'level': 2})
        id += 1
        tmp_module.append({'id': id, 'label': 'icf:' + str(module_data[modu]['icf']), 'level': 2})
        id += 1
        tmp_module.append({'id': id, 'label': 'ecf:' + str(module_data[modu]['ecf']), 'level': 2})
        id += 1
        tmp_module.append({'id': id, 'label': 'rei:' + str(module_data[modu]['rei']), 'level': 2})
        # id += 1
        # tmp_module.append({'id': id, 'label': 'chm:' + str(module_data[modu]['chm']), 'level': 2})
        # id += 1
        # tmp_module.append({'id': id, 'label': 'chd:' + str(module_data[modu]['chd']), 'level': 2})
        id += 1
        tmp_module.append({'id': id, 'label': 'DSM:' + str(module_data[modu]['DSM']), 'level': 2})
        tmp_class = list()
        for cls in module_data[modu]['classes']:
            # cls = list(module_data[modu]['classes'])[index1]
            tmp_class_metrics = list()
            # id += 1
            # tmp_class_metrics.append(
            #     {'id': id, 'label': 'c_chm:' + str(module_data[modu]['classes'][cls]['c_chm']), 'level': 4})
            # id += 1
            # tmp_class_metrics.append(
            #     {'id': id, 'label': 'c_chd:' + str(module_data[modu]['classes'][cls]['c_chd']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'CBC:' + str(module_data[modu]['classes'][cls]['CBC']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'c_FAN_IN:' + str(module_data[modu]['classes'][cls]['c_FAN_IN']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'c_FAN_OUT:' + str(module_data[modu]['classes'][cls]['c_FAN_OUT']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'IDCC:' + str(module_data[modu]['classes'][cls]['IDCC']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'IODD:' + str(module_data[modu]['classes'][cls]['IODD']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'IIDD:' + str(module_data[modu]['classes'][cls]['IIDD']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'EDCC:' + str(module_data[modu]['classes'][cls]['EDCC']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'NOP:' + str(module_data[modu]['classes'][cls]['NOP']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'NAC:' + str(module_data[modu]['classes'][cls]['NAC']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'NDC:' + str(module_data[modu]['classes'][cls]['NDC']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'NOI:' + str(module_data[modu]['classes'][cls]['NOI']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'NOID:' + str(module_data[modu]['classes'][cls]['NOID']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'RFC:' + str(module_data[modu]['classes'][cls]['RFC']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'NOSI:' + str(module_data[modu]['classes'][cls]['NOSI']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'CTM:' + str(module_data[modu]['classes'][cls]['CTM']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'c_variablesQty:' + str(module_data[modu]['classes'][cls]['c_variablesQty']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'NOM:' + str(module_data[modu]['classes'][cls]['NOM']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'WMC:' + str(module_data[modu]['classes'][cls]['WMC']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'privateMethodsQty:' + str(module_data[modu]['classes'][cls]['privateMethodsQty']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'NOVM:' + str(module_data[modu]['classes'][cls]['NOVM']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'CIS:' + str(module_data[modu]['classes'][cls]['CIS']), 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id,
                 'label': 'protectedMethodsQty:' + str(module_data[modu]['classes'][cls]['protectedMethodsQty']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'staticMethodsQty:' + str(module_data[modu]['classes'][cls]['staticMethodsQty']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'defaultMethodsQty:' + str(module_data[modu]['classes'][cls]['defaultMethodsQty']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id,
                 'label': 'abstractMethodsQty:' + str(module_data[modu]['classes'][cls]['abstractMethodsQty']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'finalMethodsQty:' + str(module_data[modu]['classes'][cls]['finalMethodsQty']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id,
                 'label': 'synchronizedMethodsQty:' + str(module_data[modu]['classes'][cls]['synchronizedMethodsQty']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'NOF:' + str(module_data[modu]['classes'][cls]['NOF']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'publicFieldsQty:' + str(module_data[modu]['classes'][cls]['publicFieldsQty']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'privateFieldsQty:' + str(module_data[modu]['classes'][cls]['privateFieldsQty']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id,
                 'label': 'protectedFieldsQty:' + str(module_data[modu]['classes'][cls]['protectedFieldsQty']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'staticFieldsQty:' + str(module_data[modu]['classes'][cls]['staticFieldsQty']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'defaultFieldsQty:' + str(module_data[modu]['classes'][cls]['defaultFieldsQty']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'finalFieldsQty:' + str(module_data[modu]['classes'][cls]['finalFieldsQty']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append({'id': id,'label': 'synchronizedFieldsQty:' + str(module_data[modu]['classes'][cls]['synchronizedFieldsQty']),
                                                         'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'TCC:' + str(module_data[modu]['classes'][cls]['TCC']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'LCC:' + str(module_data[modu]['classes'][cls]['LCC']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'LCOM:' + str(module_data[modu]['classes'][cls]['LCOM']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'LOCM*:' + str(module_data[modu]['classes'][cls]['LOCM*']),
                 'level': 4})
            id += 1
            tmp_class_metrics.append(
                {'id': id, 'label': 'c_modifiers:' + str(module_data[modu]['classes'][cls]['c_modifiers']),
                 'level': 4})
            tmp_method = list()
            for mtd in module_data[modu]['classes'][cls]['methods']:
                tmp_method_metrics = list()
                id += 1
                tmp_method_metrics.append(
                    {'id': id, 'label': 'startLine:' + str(module_data[modu]['classes'][cls]['methods'][mtd]['startLine']),
                     'level': 6})
                id += 1
                tmp_method_metrics.append(
                    {'id': id, 'label': 'CBM:' + str(module_data[modu]['classes'][cls]['methods'][mtd]['CBM']),
                     'level': 6})
                id += 1
                tmp_method_metrics.append(
                    {'id': id, 'label': 'm_FAN_IN:' + str(module_data[modu]['classes'][cls]['methods'][mtd]['m_FAN_IN']),
                     'level': 6})
                id += 1
                tmp_method_metrics.append(
                    {'id': id, 'label': 'm_FAN_OUT:' + str(module_data[modu]['classes'][cls]['methods'][mtd]['m_FAN_OUT']),
                     'level': 6})
                id += 1
                tmp_method_metrics.append(
                    {'id': id, 'label': 'IDMC:' + str(module_data[modu]['classes'][cls]['methods'][mtd]['IDMC']),
                     'level': 6})
                id += 1
                tmp_method_metrics.append(
                    {'id': id, 'label': 'EDMC:' + str(module_data[modu]['classes'][cls]['methods'][mtd]['EDMC']),
                     'level': 6})
                id += 1
                tmp_method_metrics.append(
                    {'id': id, 'label': 'methodsInvokedQty:' + str(module_data[modu]['classes'][cls]['methods'][mtd][
                                                                       'methodsInvokedQty']),
                     'level': 6})
                id += 1
                tmp_method_metrics.append(
                    {'id': id, 'label': 'methodsInvokedLocalQty:' + str(module_data[modu]['classes'][cls]['methods'][mtd][
                                                                            'methodsInvokedLocalQty']),
                     'level': 6})
                id += 1
                tmp_method_metrics.append(
                    {'id': id,
                     'label': 'methodsInvokedIndirectLocalQty:' + str(module_data[modu]['classes'][cls]['methods'][mtd][
                                                                          'methodsInvokedIndirectLocalQty']),
                     'level': 6})
                id += 1
                tmp_method_metrics.append(
                    {'id': id,
                     'label': 'm_variablesQty:' + str(module_data[modu]['classes'][cls]['methods'][mtd][
                                                          'm_variablesQty']),
                     'level': 6})
                id += 1
                tmp_method_metrics.append(
                    {'id': id,
                     'label': 'parametersQty:' + str(module_data[modu]['classes'][cls]['methods'][mtd][
                                                         'parametersQty']),
                     'level': 6})
                id += 1
                tmp_method_metrics.append(
                    {'id': id,
                     'label': 'm_modifier:' + str(module_data[modu]['classes'][cls]['methods'][mtd][
                                                      'm_modifier']),
                     'level': 6})
                id += 1
                tmp_method.append({'id': id, 'label': mtd, 'level': 5, 'children': tmp_method_metrics})
            id += 1
            tmp_class_metrics.append({'id': id, 'label': 'methods', 'level': 4, 'children': tmp_method})
            id += 1
            tmp_class.append({'id': ++id, 'label': cls, 'level': 3, 'children': tmp_class_metrics})
        id += 1
        tmp_module.append({'id': id, 'label': 'classes', 'level': 2, 'children': tmp_class})
        id += 1
        res.append({'id': id, 'label': modu, 'level': 1, 'children': tmp_module})
    result['treedata'] = res
    json_str = json.dumps(result, ensure_ascii=False)
    return JsonResponse(json_str, safe=False)


def get_scatter_data():
    # res = list()
    # with open(r'E:\test.csv', 'r') as f:
    #     csv_reader = csv.reader(f)
    #     for line in csv_reader:
    #         res.append([line[0], line[1], line[2]])
    data = pd.read_csv(r'E:\度量\tools\MicroEvaluator-main\backend\evaluator/score.csv', header=None)
    # 必须添加header=None，否则默认把第一行数据处理成列名导致缺失
    res = data.values.tolist()
    loc_level = get_level([i[1] for i in res], 'loc')
    res_dic = list()
    pro_name = list()
    for index in range(0, len(res)):
        tmp_dic = dict()
        pro_name.append(res[index][0])
        tmp_dic['x'] = res[index][1]
        tmp_dic['y'] = res[index][2]
        tmp_dic['r'] = get_r(loc_level[index])
        res_dic.append(tmp_dic)
    # res = np.insert(res, 2, values=get_level([i[1] for i in res], 'loc'), axis=1)
    # res = np.insert(res, 4, values=get_level([float(i[3]) for i in res], 'score'), axis=1)
    # res = np.insert(res, 6, values=get_level([float(i[5]) for i in res], 'scoh'), axis=1)
    # res = np.insert(res, 8, values=get_level([float(i[7]) for i in res], 'scop'), axis=1)
    # res = np.insert(res, 10, values=get_level([float(i[9]) for i in res], 'odd'), axis=1)
    # res = np.insert(res, 12, values=get_level([float(i[11]) for i in res], 'idd'), axis=1)
    # res = np.insert(res, 14, values=get_level([float(i[13]) for i in res], 'DSM'), axis=1)
    # res = np.insert(res, 0, values=['name', 'loc', 'loc_level', 'score', 'score_level'], axis=0)
    return res_dic, pro_name


def get_r(level):
    if level == 'A':
        return 20
    elif level == 'B':
        return 15
    elif level == 'C':
        return 10
    return 5


# 取基于最新两个版本的演化数据
def get_hotmap_data(request):
    result = dict()
    trend_data = pd.read_excel(r'E:\度量\tools\MicroEvaluator-main\backend\evaluator/diff_result.xlsx',
                               sheet_name='trend', engine='openpyxl')
    metrics = list(trend_data)
    metrics.remove('module_name')
    # result['hotmapdata'] = [list(trend_data['module_name']), metrics, np.array(trend_data.iloc[1:,1:]).tolist()]
    res = list()
    for index, row in trend_data.iterrows():
        res.append([index, 0, row['scoh']])
        res.append([index, 1, row['scop']])
    result['hotmapdata'] = [list(trend_data['module_name']), ['scoh', 'scop'], res]
    json_str = json.dumps(result, ensure_ascii=False)
    return JsonResponse(json_str, safe=False)


# 取基于最新两个版本的演化数据
def get_cause_entities(request):
    # data = pd.read_csv(r'E:\MicroEvaluator\backend\evaluator/causes_entities.csv', header=None)
    # data[data['module_name'] == 'com.android.server.stats']['type']
    result = dict()
    methods = list()
    id = 0
    methods = pd.read_csv(r'E:\度量\tools\MicroEvaluator-main\backend\evaluator/methods.csv', header=None)
    method_res = list()
    for index, row in methods.iterrows():
        if index == 0:
            continue
        tmp_res = list()
        id += 1
        tmp_res.append({'id': id, 'label': 'CBM:' + str(row[2]), 'level': 3})
        id += 1
        tmp_res.append({'id': id, 'label': 'startLine:' + str(row[1]), 'level': 3})
        id += 1
        tmp_res.append({'id': id, 'label': 'status:' + str(row[3]), 'level': 3})
        id += 1
        method_res.append({'id': id, 'label': row[0], 'level': 2, 'children': tmp_res})
    id += 1
    result['causes'] = [{'type': 'call',
                         'entities': [{'id': id, 'label': 'com.android.server.stats.StatsCompanionService', 'level': 1,
                                       'children': method_res}]}]
    json_str = json.dumps(result, ensure_ascii=False)
    return JsonResponse(json_str, safe=False)
