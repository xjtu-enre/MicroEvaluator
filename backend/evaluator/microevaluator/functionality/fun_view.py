# from evaluator.models import EvaluatorAvgData
# from project.data_view import query_data_from_project_detail, save_to_project_detail


# def get_all_Data_functionality(token, projectname, projecturl, numOfPlan, type):
#     [tracefilename, classfileName, structdepFile, conceptdepFile,
#             commitFileName, rulesfile, min_support,
#             min_confidence, fileType, apiFileName, serviceFileName] = initialization(projectname, 1, type)
#
#     [CHM, IFN, chmdict, ifndict] = chm(serviceFileName, apiFileName, fileType)  # chmdict is chm for each service
#     [CHD, IFN, chddict, servicenumwhohasinf] = chd(serviceFileName, apiFileName, fileType)
#
#     return dict()


# '''
#     functionality
# '''
# 将方案对比、ifn、chd、chm的所有数据放在allData中，最后直接将其返回给前台
# def get_all_data_functionality(project_name, version, owner):
#     all_data = dict()
#     metrics = dict()
#     plan_num = []
#     radar_data = []
#     project_data = ProjectData.objects.filter(projectname=project_name, version=version, owner=owner).first()
#     for number_of_plan in range(0, project_data.plancount):
#         # 先在库内查询，如果能够查到该项目该方案的数据，直接查询返回；若查不到，重新计算入库
#         project_data = ProjectData.objects.filter(projectname=project_name, plannum=number_of_plan + 1,
#                                                   owner=owner, version=version)
#         if project_data.exists():
#             if project_data.first().CHM != 0:
#                 CHM = project_data.first().CHM
#                 CHD = project_data.first().CHD
#                 IFN = project_data.first().IFN
#
#                 chmdict = query_data_from_project_detail(project_name, number_of_plan + 1, 'chm', owner, version)
#                 chddict = query_data_from_project_detail(project_name, number_of_plan + 1, 'chd', owner, version)
#                 ifndict = query_data_from_project_detail(project_name, number_of_plan + 1, 'ifn', owner, version)
#
#             else:
#                 [trace_file, class_file, struct_dep_file, concept_dep_file, commit_file, rules_file, min_support,
#                  min_confidence, file_ype, api_file, service_file] = initialization(project_name, number_of_plan + 1,
#                                                                                     version)
#
#                 [CHM, IFN, chmdict, ifndict] = chm(service_file, api_file,
#                                                    file_ype)  # chmdict is chm for each service
#                 [CHD, IFN, chddict, servicenumwhohasinf] = chd(service_file, api_file, file_ype)
#
#                 # CHM、CHD、IFN
#                 project_data.update(CHM=format(float(CHM), '.4f'), CHD=format(float(CHD), '.4f'),
#                                     IFN=format(float(IFN), '.4f'))
#                 # chddict、chmdict、ifndict
#                 save_to_project_detail(chmdict, number_of_plan + 1, 'chm', project_name, owner, version)
#                 save_to_project_detail(chddict, number_of_plan + 1, 'chd', project_name, owner, version)
#                 save_to_project_detail(ifndict, number_of_plan + 1, 'ifn', project_name, owner, version)
#             current_plan_dic = dict()
#             current_plan_dic['value'] = [CHM, CHD, IFN]
#             current_plan_dic['name'] = 'plan' + str(number_of_plan + 1)
#             radar_data.append(current_plan_dic)
#             plan_num.append('plan' + str(number_of_plan + 1))
#
#             metrics_dic = list()
#             risk_services_dic = dict()
#             # ifn
#             ifn_temp = []
#             for key in ifndict:
#                 ifn_temp.append(float(ifndict[key]))
#                 metrics_dic.append([key])
#             metrics_dic = np.insert(metrics_dic, 0, ifn_temp, axis=1)
#             # ifn_risk_services = set(get_risk_servies(ifn_temp, 'ifn', dic))
#
#             # chm
#             chm_temp = []
#             for key in chmdict.keys():
#                 chm_temp.append(float(chmdict[key]))
#             # chm_risk_services = set(get_risk_servies(chm_temp, 'chm', dic))
#             metrics_dic = np.insert(metrics_dic, 1, chm_temp, axis=1)
#
#             # chd
#             chd_temp = []
#             for key in chddict.keys():
#                 chd_temp.append(float(chddict[key]))
#             # chd_risk_services = set(get_risk_servies(chd_temp, 'chd', dic))
#             metrics_dic = np.insert(metrics_dic, 2, chd_temp, axis=1)
#             metrics_dic = np.insert(metrics_dic, 0, ['ifn', 'chm', 'chd', 'servicename'], axis=0)
#
#             # 求chm_risk_services和chd_risk_services的交集,再求其与ifn_risk_services的并集
#             # risk_services = ifn_risk_services | (chm_risk_services & chd_risk_services)
#
#             # 获取该方案的指标集合
#             metrics['plan' + str(number_of_plan + 1)] = metrics_dic.tolist()
#             # 获取该方案的风险集合
#             # risk_services_dic['plan' + str(number_of_plan + 1)] = list(risk_services)
#         else:
#             all_data['status'] = 'error'
#             return all_data
#
#     indicator_data = [{'name': 'CHM'}, {'name': 'CHD'}, {'name': 'IFN'}]
#     plan_dic = dict()
#     plan_dic['planNum'] = plan_num
#     plan_dic['radarData'] = radar_data
#     plan_dic['indicatorData'] = indicator_data
#
#     all_data['funplanData'] = plan_dic
#     all_data['metrics'] = metrics
#     all_data['funRiskServices'] = risk_services_dic
#     all_data['status'] = 'ok'
#
#     return all_data
