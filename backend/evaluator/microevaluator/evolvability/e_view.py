# from evaluator.models import EvaluatorAvgData
# from project.data_view import query_data_from_project_detail, save_to_project_detail, save_rei_to_db


def get_all_data_evolvability(project_name, version, owner):
    all_data = dict()
    # metrics = dict()
    # plan_num = []
    # radar_data = []
    # project_data = EvaluatorAvgData.objects.filter(projectname=project_name, version=version, owner=owner).first()
    # for number_of_plan in range(0, project_data.plancount):
    #     # 先在库内查询，如果能够查到该项目该方案的数据，直接查询返回；若查不到，重新计算入库
    #     project_data = EvaluatorAvgData.objects.filter(projectname=project_name, plannum=number_of_plan + 1,
    #                                               owner=owner, version=version)
    #     if project_data.exists():
    #         if project_data.first().ICF != 0:
    #             ICF = project_data.first().ICF
    #             ECF = project_data.first().ECF
    #             REI = project_data.first().REI
    #             FOCUS = project_data.first().FOCUS
    #             SPREAD = project_data.first().SPREAD
    #
    #             icfdict = query_data_from_project_detail(project_name, number_of_plan + 1, 'icf', owner,
    #                                                      version)
    #             ecfdict = query_data_from_project_detail(project_name, number_of_plan + 1, 'ecf', owner,
    #                                                      version)
    #             focusdict = query_data_from_project_detail(project_name, number_of_plan + 1, 'focus', owner,
    #                                                        version)
    #             spreaddict = query_data_from_project_detail(project_name, number_of_plan + 1, 'spread', owner,
    #                                                         version)
    #         else:
    #             [trace_file, class_file, struct_dep_file, concept_dep_file, commit_file, rules_file, min_support,
    #              min_confidence, file_ype, api_file, service_file] = initialization(project_name, number_of_plan + 1,
    #                                                                                 version)
    #
    #             [ICF, ECF, REI, icfdict, ecfdict] = ioe(commit_file, file_ype, service_file)
    #             focusdict, spreaddict, FOCUS, SPREAD = sf(commit_file, service_file)
    #
    #             # ICF/ECF/REI
    #             project_data.update(ICF=format(float(ICF), '.4f'), ECF=format(float(ECF), '.4f'),
    #                                 REI=format(float(REI), '.4f'), FOCUS=format(float(FOCUS), '.4f'),
    #                                 SPREAD=format(float(SPREAD), '.4f'))
    #
    #             # icfdict/ecfdict
    #             save_to_project_detail(icfdict, number_of_plan + 1, 'icf', project_name, owner, version)
    #             save_to_project_detail(ecfdict, number_of_plan + 1, 'ecf', project_name, owner, version)
    #             # rei
    #             save_rei_to_db(icfdict, ecfdict, number_of_plan + 1, 'rei', project_name, owner, version)
    #             # focus/spread
    #             save_to_project_detail(focusdict, number_of_plan + 1, 'focus', project_name, owner, version)
    #             save_to_project_detail(spreaddict, number_of_plan + 1, 'spread', project_name, owner, version)
    #
    #         current_plan_dic = dict()
    #         current_plan_dic['value'] = [ICF, ECF, REI, FOCUS, SPREAD]
    #         current_plan_dic['name'] = 'plan' + str(number_of_plan + 1)
    #         radar_data.append(current_plan_dic)
    #         plan_num.append('plan' + str(number_of_plan + 1))
    #
    #         metrics_dic = list()
    #         risk_services_dic = dict()
    #         # icf
    #         icftemp = []
    #         for key in icfdict:
    #             metrics_dic.append([key])
    #             icftemp.append(format(float(icfdict[key]), '.4f'))
    #         metrics_dic = np.insert(metrics_dic, 0, icftemp, axis=1)
    #
    #         # ecf
    #         ecftemp = []
    #         for key in ecfdict:
    #             ecftemp.append(format(float(ecfdict[key]), '.4f'))
    #         metrics_dic = np.insert(metrics_dic, 1, ecftemp, axis=1)
    #
    #         # rei:rei=ecf/icf;如果icf=0,则rei值为无穷大
    #         risk_services = []
    #         reitemp = []
    #         for service_value in metrics_dic:
    #             if float(service_value[0]) == 0:
    #                 # 用-1来代表无穷大
    #                 reitemp.append(-1)
    #                 continue
    #             reitemp.append(format(float(service_value[1]) / float(service_value[0]), '.4f'))
    #             # rei大于1即为有风险微服务
    #             # if dic['rows'][number]['rei'] > 1:
    #             #     dic['rows'][number]['isRisk'] = True
    #             #     risk_services.append(service_name[number])
    #             # else:
    #             #     dic['rows'][number]['isRisk'] = False
    #         metrics_dic = np.insert(metrics_dic, 2, reitemp, axis=1)
    #
    #         # focus:越大越好
    #         focustemp = []
    #         for key in focusdict:
    #             focustemp.append(format(float(focusdict[key]), '.4f'))
    #         metrics_dic = np.insert(metrics_dic, 3, focustemp, axis=1)
    #
    #         # sperad:越小越好
    #         spreadtemp = []
    #         for key in spreaddict:
    #             spreadtemp.append(format(float(spreaddict[key]), '.4f'))
    #         metrics_dic = np.insert(metrics_dic, 4, spreadtemp, axis=1)
    #
    #         metrics_dic = np.insert(metrics_dic, 0, ['icf', 'ecf', 'rei', 'focus', 'spread', 'servicename'], axis=0)
    #
    #         # 获取指标集合
    #         metrics['plan' + str(number_of_plan + 1)] = metrics_dic.tolist()
    #         # 获取风险集合
    #         risk_services_dic['plan' + str(number_of_plan + 1)] = list(risk_services)
    #     else:
    #         all_data['status'] = 'error'
    #         return all_data
    #
    # indicator_data = [{'name': 'ICF'}, {'name': 'ECF'}, {'name': 'REI'}, {'name': 'FOCUS'}, {'name': 'SPERAD'}]
    # plan_dic = dict()
    # plan_dic['planNum'] = plan_num
    # plan_dic['radarData'] = radar_data
    # plan_dic['indicatorData'] = indicator_data
    #
    # all_data['eplanData'] = plan_dic
    # all_data['metrics'] = metrics
    # all_data['eRiskServices'] = risk_services_dic
    # all_data['status'] = 'ok'

    return all_data
