# from evaluator.models import EvaluatorAvgData
# from project.data_view import query_data_from_project_detail, save_to_project_detail


def get_all_data_modularity(project_name, version, owner):
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
    #         if project_data.first().SMQ != 0:
    #             SMQ = project_data.first().SMQ
    #             CMQ = project_data.first().CMQ
    #
    #             scohList = query_data_from_project_detail(project_name, number_of_plan + 1, 'scoh', owner,
    #                                                       version)
    #             scopList = query_data_from_project_detail(project_name, number_of_plan + 1, 'scop', owner,
    #                                                       version)
    #             ccohList = query_data_from_project_detail(project_name, number_of_plan + 1, 'ccoh', owner,
    #                                                       version)
    #             ccopList = query_data_from_project_detail(project_name, number_of_plan + 1, 'ccop', owner,
    #                                                       version)
    #         else:
    #             [trace_file, class_file, struct_dep_file, concept_dep_file, commit_file, rules_file, min_support,
    #              min_confidence, file_ype, api_file, service_file] = initialization(project_name, number_of_plan + 1,
    #                                                                                 version)
    #
    #             [SMQ, CMQ, scohList, scopList, ccohList, ccopList, servienames] = mq(struct_dep_file, concept_dep_file,
    #                                                                                  service_file)
    #
    #             # SMQ、CMQ
    #             project_data.update(SMQ=format(float(SMQ), '.4f'), CMQ=format(float(CMQ), '.4f'))
    #
    #             # scohList/scopList/ccohList/ccopList
    #             scohList = dict(zip(servienames, scohList))
    #             scopList = dict(zip(servienames, scopList))
    #             ccohList = dict(zip(servienames, ccohList))
    #             ccopList = dict(zip(servienames, ccopList))
    #             save_to_project_detail(scohList, number_of_plan + 1, 'scoh', project_name, owner, version)
    #             save_to_project_detail(scopList, number_of_plan + 1, 'scop', project_name, owner, version)
    #             save_to_project_detail(ccohList, number_of_plan + 1, 'ccoh', project_name, owner, version)
    #             save_to_project_detail(ccopList, number_of_plan + 1, 'ccop', project_name, owner, version)
    #
    #         current_plan_dic = dict()
    #         current_plan_dic['value'] = [format(float(SMQ), '.4f'), format(float(CMQ), '.4f')]
    #         current_plan_dic['name'] = 'plan' + str(number_of_plan + 1)
    #         radar_data.append(current_plan_dic)
    #         plan_num.append('plan' + str(number_of_plan + 1))
    #
    #         metrics_dic = list()
    #         risk_services_dic = dict()
    #         # scoh
    #         scoh_temp = []
    #         for key in scohList:
    #             scoh_temp.append(format(float(scohList[key]), '.4f'))
    #             metrics_dic.append([key])
    #         metrics_dic = np.insert(metrics_dic, 0, scoh_temp, axis=1)
    #         # scoh_risk_services = set(get_risk_servies(scoh_temp, 'scoh', dic))
    #
    #         # scop
    #         scop_temp = []
    #         for key in scopList:
    #             scop_temp.append(format(float(scopList[key]), '.4f'))
    #         metrics_dic = np.insert(metrics_dic, 1, scop_temp, axis=1)
    #         # scop_risk_services = set(get_risk_servies(scop_temp, 'scop', dic))
    #
    #         # ccoh
    #         ccoh_temp = []
    #         for key in ccohList:
    #             ccoh_temp.append(format(float(ccohList[key]), '.4f'))
    #         metrics_dic = np.insert(metrics_dic, 2, ccoh_temp, axis=1)
    #         # ccoh_risk_services = set(get_risk_servies(ccoh_temp, 'ccoh', dic))
    #
    #         # ccop
    #         ccop_temp = []
    #         for key in ccopList:
    #             ccop_temp.append(format(float(ccopList[key]), '.4f'))
    #         metrics_dic = np.insert(metrics_dic, 3, ccoh_temp, axis=1)
    #         metrics_dic = np.insert(metrics_dic, 0, ['scoh', 'scop', 'ccoh', 'ccop', 'servicename'], axis=0)
    #         # ccop_risk_services = set(get_risk_servies(ccop_temp, 'ccop', dic))
    #
    #         # 获取指标的集合
    #         metrics['plan' + str(number_of_plan + 1)] = metrics_dic.tolist()
    #         # 获取该方案的风险集合
    #         # risk_services = scoh_risk_services | scop_risk_services | ccoh_risk_services | ccop_risk_services
    #         # risk_services_dic['plan' + str(number_of_plan + 1)] = list(risk_services)
    #     else:
    #         all_data['status'] = 'error'
    #         return all_data
    #
    # indicator_data = [{'name': 'SMQ'}, {'name': 'CMQ'}]
    # plan_dic = dict()
    # plan_dic['planNum'] = plan_num
    # plan_dic['radarData'] = radar_data
    # plan_dic['indicatorData'] = indicator_data
    #
    # all_data['mplanData'] = plan_dic
    # all_data['metrics'] = metrics
    # all_data['mRiskServices'] = risk_services_dic
    # all_data['status'] = 'ok'

    return all_data
