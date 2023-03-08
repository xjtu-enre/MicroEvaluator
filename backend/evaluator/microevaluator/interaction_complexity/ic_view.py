# from evaluator.models import EvaluatorAvgData
# from project.data_view import query_data_from_project_detail, save_to_project_detail


def get_all_Data_InteractionComplexity(project_name, version, owner):
    all_data = dict()
    # metrics = dict()
    # plan_dic = {'columns': ['参数类型'],
    #             'rows': [{'参数类型': 'ODD'}, {'参数类型': 'IDD'}, {'参数类型': 'SCN'}, {'参数类型': 'ISG'}, {'参数类型': 'ICL'}]}
    # for number_of_plan in range(0, 1):
    #     # 先在库内查询，如果能够查到该项目该方案的数据，直接查询返回；若查不到，重新计算入库
    #     projectdata = EvaluatorAvgData.objects.filter(projectname=project_name, plannum='plan' + str(number_of_plan + 1))
    #     if projectdata.exists() and not projectdata.first().ODD == 0:
    #         ODD = projectdata.first().ODD
    #         IDD = projectdata.first().IDD
    #         ISG = projectdata.first().ISG
    #         ICL = projectdata.first().ICL
    #         SCN = projectdata.first().SCN
    #
    #         odddict = query_data_from_project_detail(project_name, 'plan' + str(number_of_plan + 1), 'odd')
    #         idddict = query_data_from_project_detail(project_name, 'plan' + str(number_of_plan + 1), 'idd')
    #         isgdict = query_data_from_project_detail(project_name, 'plan' + str(number_of_plan + 1), 'isg')
    #         icldict = query_data_from_project_detail(project_name, 'plan' + str(number_of_plan + 1), 'icl')
    #     else:
    #         [trace_file, class_file, struct_dep_file, concept_dep_file, commit_file, rules_file, min_support,
    #          min_confidence, file_ype, api_file, service_file] = initialization(project_name, number_of_plan + 1,
    #                                                                             version)
    #         [ODD, IDD, ODD_nouse, IDD_nouse, SCN, DSM_probability, odddict, idddict, cyclelist,
    #          servicelist] = odd_idd_scn(rules_file, service_file, trace_file, min_support, min_confidence)
    #         # [ISG, ICL, isgdict, icldict, DSM_behavior, traceIDList] = icl_isg(serviceFileName, tracefilename)
    #         ISG = 0
    #         ICL = 0
    #         isgdict = {}
    #         icldict = {}
    #         # 处理特殊情况：isg和icl可能存在在某个微服务没有值
    #         for service in servicelist:
    #             if service not in odddict:
    #                 odddict[service] = 0
    #             if service not in idddict:
    #                 idddict[service] = 0
    #
    #         # ODD/IDD/ISG/ICL/SCN
    #         if not projectdata.exists():
    #             projectdata.create(projectname=project_name, plannum='plan' + str(number_of_plan + 1), ODD=ODD, IDD=IDD,
    #                                ISG=ISG, ICL=ICL, SCN=SCN)
    #         else:
    #             projectdata.update(ODD=ODD, IDD=IDD, ISG=ISG, ICL=ICL, SCN=SCN)
    #
    #         # odddict/idddict/isgdict/icldict（isg、icl的servicename是其轨迹编号，不影响后面使用）
    #         save_to_project_detail(odddict, 'plan' + str(number_of_plan + 1), 'odd', project_name, 'test', owner,
    #                                version)
    #         save_to_project_detail(idddict, 'plan' + str(number_of_plan + 1), 'idd', project_name, 'test', owner,
    #                                version)
    #         save_to_project_detail(isgdict, 'plan' + str(number_of_plan + 1), 'isg', project_name, 'test', owner,
    #                                version)
    #         save_to_project_detail(icldict, 'plan' + str(number_of_plan + 1), 'icl', project_name, 'test', owner,
    #                                version)
    #
    #     # plan
    #     plan_dic['columns'].append('plan' + str(number_of_plan + 1))
    #     plan_dic['rows'][0]['plan' + str(number_of_plan + 1)] = ODD
    #     plan_dic['rows'][1]['plan' + str(number_of_plan + 1)] = IDD
    #     plan_dic['rows'][2]['plan' + str(number_of_plan + 1)] = SCN
    #     plan_dic['rows'][3]['plan' + str(number_of_plan + 1)] = ISG
    #     plan_dic['rows'][4]['plan' + str(number_of_plan + 1)] = ICL
    #
    #     metrics_dic = dict()
    #     risk_services_dic = dict()
    #     # odd
    #     odd_temp = []
    #     dic = {'columns': ['name', 'odd'], 'rows': []}
    #     for number in range(0, len(list(odddict.keys()))):
    #         dic['rows'].append({'name': list(odddict.keys())[number]})
    #         dic['rows'][number]['odd'] = odddict[list(odddict.keys())[number]]
    #         dic['rows'][number]['isRisk'] = False
    #         odd_temp.append(odddict[list(odddict.keys())[number]])
    #
    #     odd_risk_services = set(get_risk_servies(odd_temp, 'odd', dic))
    #     metrics_dic['odd'] = dic
    #
    #     # idd
    #     idd_temp = []
    #     dic = {'columns': ['name', 'idd'], 'rows': []}
    #     for number in range(0, len(list(idddict.keys()))):
    #         dic['rows'].append({'name': list(idddict.keys())[number]})
    #         dic['rows'][number]['idd'] = idddict[list(idddict.keys())[number]]
    #         dic['rows'][number]['isRisk'] = False
    #         idd_temp.append(idddict[list(idddict.keys())[number]])
    #
    #     idd_risk_services = set(get_risk_servies(idd_temp, 'idd', dic))
    #     metrics_dic['idd'] = dic
    #
    #     # isg
    #     dic = {'columns': ['name', 'isg'], 'rows': []}
    #     for number in range(0, len(list(isgdict.keys()))):
    #         dic['rows'].append({'name': list(isgdict.keys())[number]})
    #         dic['rows'][number]['isg'] = isgdict[list(isgdict.keys())[number]]
    #     metrics_dic['isg'] = dic
    #
    #     # icl
    #     dic = {'columns': ['name', 'icl'], 'rows': []}
    #     for number in range(0, len(list(icldict.keys()))):
    #         dic['rows'].append({'name': list(icldict.keys())[number]})
    #         dic['rows'][number]['icl'] = icldict[list(icldict.keys())[number]]
    #     metrics_dic['icl'] = dic
    #
    #     # 获取指标集合
    #     metrics['plan' + str(number_of_plan + 1)] = metrics_dic
    #     # 获取风险集合
    #     risk_services = odd_risk_services | idd_risk_services
    #     risk_services_dic['plan' + str(number_of_plan + 1)] = list(risk_services)
    #
    # all_data['icplanData'] = plan_dic
    # all_data['metrics'] = metrics
    # all_data['icRiskServices'] = risk_services_dic

    return all_data
