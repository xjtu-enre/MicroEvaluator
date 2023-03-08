import csv
import os
import numpy as np

# from evaluator.models import EvaluatorAvgData, EvaluatorDetailData
from project.models import Project
from evaluator.utils.boxplot import get_percent
# from project.data_view import query_data_from_projectdetaildata


def get_project_data(owner):
    # 为当前用户下未计算评分的项目计算评分
    # compete_all_score(owner, weight, typenames)
    # 从数据库中查询所有已经计算过综合评分的项目数据，return：[score, loc(项目级), IFN, CHM, CHD, ICF, ECF]
    dic = dict()
    all_data = list()
    loc = list()
    score = list()
    pro_msg = list()
    IFN = list()
    CHM = list()
    CHD = list()
    ICF = list()
    ECF = list()

    projects = Project.objects.filter(owner=owner)
    for index in range(0, len(projects)):
        # 每次拿所有版本的最新版本
        project = Project.objects.filter(owner=owner, projectname=projects[index].projectname).first()
        len_version = len(project.version.split(';'))
        lastest_version = project.version.split(';')[len_version - 1]
        # project_data = EvaluatorAvgData.objects.filter(owner=owner, projectname=projects[index].projectname,
        #                                           version=lastest_version).first()

        # get_all_data_functionality(project_data.projectname, project_data.version, owner)
        # get_all_data_modularity(project_data.projectname, project_data.version, owner)
        # get_all_data_evolvability(project_data.projectname, project_data.version, owner)
        # weight = [0.1112, 0.1111, 0.1111, 0.1111, 0.1111, 0.1111, 0.1111, 0.1111, 0.1111]
        # type_names = ['ifn', 'chm', 'chd', 'icf', 'ecf', 'scoh', 'scop', 'ccoh', 'ccop']
        # compete_one_score(owner, weight, project_data.version, type_names, project_data.projectname)

        # 若没有接口数据或者综合评分，不予展示
        # if project_data.score == 0 or project_data.IFN == 0:
        #     continue
        # pro_msg.append(
        #     {'index': index + 1, 'projectname': project_data.projectname,
        #      'services': project_data.services,
        #      'url': projects[index].url,
        #      'score': project_data.score})
        # single_data = list()
        # # projectdata = query_data_from_project_data(projects_data[index].projectname,
        # #                                            projects_data[index].numberOfPlan)
        # single_data.append(int(project_data.loc))
        # single_data.append(project_data.IFN)
        # single_data.append(project_data.CHM)
        # single_data.append(project_data.CHD)
        # single_data.append(project_data.ICF)
        # single_data.append(project_data.ECF)
        # single_data.append(project_data.score)
        # single_data.append(project_data.projectname)
        # single_data.append(index + 1)
        # loc.append(int(project_data.loc))
        # IFN.append(project_data.IFN)
        # CHM.append(project_data.CHM)
        # CHD.append(project_data.CHD)
        # ICF.append(project_data.ICF)
        # ECF.append(project_data.ECF)
        # score.append(project_data.score)

        # all_data.append(single_data)

    #  对库中所有项目指标进行分级
    all_data = np.insert(all_data, 1, values=_get_level(loc, 'loc'), axis=1)
    all_data = np.insert(all_data, 3, values=_get_level(IFN, 'IFN'), axis=1)
    all_data = np.insert(all_data, 5, values=_get_level(CHM, 'CHM'), axis=1)
    all_data = np.insert(all_data, 7, values=_get_level(CHD, 'CHD'), axis=1)
    all_data = np.insert(all_data, 9, values=_get_level(ICF, 'ICF'), axis=1)
    all_data = np.insert(all_data, 11, values=_get_level(ECF, 'ECF'), axis=1)
    all_data = np.insert(all_data, 13, values=_get_level(score, 'score'), axis=1)

    # 给项目信息中插入项目等级=score_level
    insert_level(pro_msg, all_data)
    # # 结合项目信息和每个服务评分，获取服务质量分析结果返回给前台
    # all_services_count, all_count = get_reasons(pro_msg, owner)

    #  再插入表头
    all_data = np.insert(all_data, 0,
                         values=['loc', 'loc_level', 'IFN', 'IFN_level', 'CHM', 'CHM_level', 'CHD', 'CHD_level', 'ICF',
                                 'ICF_level', 'ECF', 'ECF_level', 'score', 'score_level', 'projectname',
                                 'projectindex'], axis=0)
    dic['allData'] = all_data.tolist()

    return dic, pro_msg


def insert_level(pro_msg, all_data):
    if len(pro_msg) == len(all_data):
        for index in range(0, len(all_data)):
            pro_msg[index]['level'] = all_data[index][13]


def get_micro_data(owner, pro_msg):
    micro_dic = dict()
    all_data = list()
    loc = list()
    ifn = list()
    chm = list()
    chd = list()
    icf = list()
    ecf = list()

    # projects = Project.objects.filter(owner=owner)
    all_services_count = [0 for col in range(10)]
    all_count = 0
    # for index1 in range(0, len(projects)):
    #     # print(projects[index1].projectname)
    #     project_data = EvaluatorAvgData.objects.filter(projectname=projects[index1].projectname, owner=owner).first()
    #
    #     # 没有接口的暂时不予显示
    #     if project_data.services == '' or project_data.serviceloc == '' or project_data.IFN == 0:
    #         continue
    #     services = project_data.services.split(';')
    #     service_loc = project_data.serviceloc.split(';')
    #
    #     if len(services) == len(service_loc):
    #         single_metric = list()
    #         for index2 in range(0, len(services)):
    #             # print(data.Project)
    #             # 方案暂不考虑
    #             ifn_value = query_data_from_projectdetaildata(project_data.projectname, services[index2], 'ifn',
    #                                                           project_data.version, owner).value
    #             chm_value = query_data_from_projectdetaildata(project_data.projectname, services[index2], 'chm',
    #                                                           project_data.version, owner).value
    #             chd_value = query_data_from_projectdetaildata(project_data.projectname, services[index2], 'chd',
    #                                                           project_data.version, owner).value
    #             icf_value = query_data_from_projectdetaildata(project_data.projectname, services[index2], 'icf',
    #                                                           project_data.version, owner).value
    #             ecf_value = query_data_from_projectdetaildata(project_data.projectname, services[index2], 'ecf',
    #                                                           project_data.version, owner).value
    #             scoh_value = query_data_from_projectdetaildata(project_data.projectname, services[index2], 'scoh',
    #                                                            project_data.version, owner).value
    #             scop_value = query_data_from_projectdetaildata(project_data.projectname, services[index2], 'scop',
    #                                                            project_data.version, owner).value
    #             ccoh_value = query_data_from_projectdetaildata(project_data.projectname, services[index2], 'ccoh',
    #                                                            project_data.version, owner).value
    #             ccop_value = query_data_from_projectdetaildata(project_data.projectname, services[index2], 'ccop',
    #                                                            project_data.version, owner).value
    #             all_data.append(
    #                 [service_loc[index2], ifn_value, chm_value, chd_value, icf_value, ecf_value, services[index2],
    #                  index1 + 1])
    #             loc.append(int(service_loc[index2]))
    #             single_metric.append(
    #                 [services[index2], ifn_value, chm_value, chd_value, icf_value, ecf_value, scoh_value, scop_value,
    #                  ccoh_value, ccop_value])
    #             ifn.append(ifn_value)
    #             chm.append(chm_value)
    #             chd.append(chd_value)
    #             icf.append(icf_value)
    #             ecf.append(ecf_value)
    #             all_count += 1
    #
    #         # # 对单个服务各个指标计算箱线图结果，对其中异常值和较低值进行标注
    #         # all_services_count = get_reasons(pro_msg, single_metric, project_data.projectname, all_services_count,
    #         #                                  project_data.version, owner)
    #     else:
    #         continue
    #
    # #  对所有服务的指标进行评级
    # all_data = np.insert(all_data, 1, values=_get_level(loc, 'loc'), axis=1)
    # all_data = np.insert(all_data, 3, values=_get_level(ifn, 'ifn'), axis=1)
    # all_data = np.insert(all_data, 5, values=_get_level(chm, 'chm'), axis=1)
    # all_data = np.insert(all_data, 7, values=_get_level(chd, 'chd'), axis=1)
    # all_data = np.insert(all_data, 9, values=_get_level(icf, 'icf'), axis=1)
    # all_data = np.insert(all_data, 11, values=_get_level(ecf, 'ecf'), axis=1)
    #
    # #  再插入表头
    # all_data = np.insert(all_data, 0,
    #                      values=['loc', 'loc_level', 'ifn', 'ifn_level', 'chm', 'chm_level', 'chd', 'chd_level', 'icf',
    #                              'icf_level', 'ecf', 'ecf_level', 'servicename', 'projectindex'], axis=0)
    #
    # micro_dic['allData'] = all_data.tolist()

    return micro_dic, all_services_count, all_count


def get_reasons(pro_msg, single_metric, project_name, all_services_count, version, owner):
    for pro in pro_msg:
        if pro['projectname'] == project_name:
            services_score = dict()
            file_path = '.\\evaluator\\data\\UploadData\\' + owner + '\\' + project_name + '\\' + version + '\\output.csv'
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                for line in reader:
                    temp = line[0].split(' ')
                    services_score[temp[0]] = format(float(temp[10]), '.4f')

                tags, reasons, reasons_count, services_levels = get_services_info(single_metric, len(single_metric),
                                                                                  all_services_count)
            pro['reasonscount'] = reasons_count
            pro['tags'] = tags
            pro['reasons'] = reasons
            pro['levels'] = services_levels
            pro['servicesscore'] = services_score
            pro['maxcount'] = len(single_metric)
            break
    return all_services_count


def get_tags_and_reasons(metric_score, all_percent, service_len, all_services_count):
    services_reasons = dict()
    services_tags = dict()
    services_levels = dict()
    services_reasons_count = [0 for col in range(10)]

    for metric in metric_score:
        single_tags = list()
        single_reasons = list()
        services_reasons_level = list()
        if float(metric[1]) > all_percent[0][2]:
            if '功能内聚' not in single_tags:
                single_tags.append('功能内聚')
            if float(metric[1]) > all_percent[0][3]:
                single_reasons.append('ifn：该微服务是一个web应用(或对外提供的API过多)')
                services_reasons_level.append('danger')
            else:
                single_reasons.append('ifn：该微服务是一个web应用(或对外提供的API较多)')
                services_reasons_level.append('warning')
            services_reasons_count[0] += 1
            all_services_count[0] += 1
        if float(metric[2]) < all_percent[1][0]:
            if '功能内聚' not in single_tags:
                single_tags.append('功能内聚')
            if float(metric[2]) < all_percent[1][4]:
                single_reasons.append('chm：接口函数比较少但大于1，输入消息和输出消息相似性过低')
                services_reasons_level.append('danger')
            else:
                single_reasons.append('chm：接口函数比较少但大于1，输入消息和输出消息相似性较低')
                services_reasons_level.append('warning')
            services_reasons_count[1] += 1
            all_services_count[1] += 1
        if float(metric[3]) < all_percent[2][0]:
            if '功能内聚' not in single_tags:
                single_tags.append('功能内聚')
            if float(metric[3]) < all_percent[2][4]:
                single_reasons.append('chd：接口函数比较少但大于1，不同方法之间的签名相似性过低')
                services_reasons_level.append('danger')
            else:
                single_reasons.append('chd：接口函数比较少但大于1，不同方法之间的签名相似性较低')
                services_reasons_level.append('warning')
            services_reasons_count[2] += 1
            all_services_count[2] += 1
        if float(metric[4]) < all_percent[3][0]:
            if '演化历史' not in single_tags:
                single_tags.append('演化历史')
            if float(metric[4]) < all_percent[3][4]:
                single_reasons.append('icf：该微服务内部共同演化程度过低')
                services_reasons_level.append('danger')
            else:
                single_reasons.append('icf：该微服务内部共同演化程度较低')
                services_reasons_level.append('warning')
            services_reasons_count[3] += 1
            all_services_count[3] += 1
        if float(metric[5]) > all_percent[4][2]:
            if '演化历史' not in single_tags:
                single_tags.append('演化历史')
            if float(metric[5]) > all_percent[4][3]:
                single_reasons.append('ecf：该微服务与外部服务一起演化的可能性过高')
                services_reasons_level.append('danger')
            else:
                single_reasons.append('ecf：该微服务与外部服务一起演化的可能性更高')
                services_reasons_level.append('warning')
            services_reasons_count[4] += 1
            all_services_count[4] += 1
        if float(metric[6]) < all_percent[5][0]:
            if '结构依赖' not in single_tags:
                single_tags.append('结构依赖')
            if float(metric[6]) < all_percent[5][4]:
                single_reasons.append('scoh：该微服务内部结构依赖程度过低')
                services_reasons_level.append('danger')
            else:
                single_reasons.append('scoh：该微服务内部结构依赖程度较低')
                services_reasons_level.append('warning')
            services_reasons_count[5] += 1
            all_services_count[5] += 1
        if float(metric[7]) > all_percent[6][2]:
            if '结构依赖' not in single_tags:
                single_tags.append('结构依赖')
            if float(metric[7]) > all_percent[6][3]:
                single_reasons.append('scop：该微服务对外部服务结构依赖程度过高')
                services_reasons_level.append('danger')
            else:
                single_reasons.append('scop：该微服务对外部服务结构依赖程度较高')
                services_reasons_level.append('warning')
            services_reasons_count[6] += 1
            all_services_count[6] += 1
        if float(metric[8]) < all_percent[7][0]:
            if '语义依赖' not in single_tags:
                single_tags.append('语义依赖')
            if float(metric[8]) < all_percent[7][4]:
                single_reasons.append('ccoh：该微服务内部语义依赖程度过低')
                services_reasons_level.append('danger')
            else:
                single_reasons.append('ccoh：该微服务内部语义依赖程度较低')
                services_reasons_level.append('warning')
            services_reasons_count[7] += 1
            all_services_count[7] += 1
        if float(metric[9]) > all_percent[8][2]:
            if '语义依赖' not in single_tags:
                single_tags.append('语义依赖')
            if float(metric[9]) > all_percent[8][3]:
                single_reasons.append('ccop：该微服务与外部服务语义依赖程度过高')
                services_reasons_level.append('danger')
            else:
                single_reasons.append('ccop：该微服务与外部服务语义依赖程度较高')
                services_reasons_level.append('warning')
            services_reasons_count[8] += 1
            all_services_count[8] += 1
        if service_len < 4:
            single_tags.append('项目特征')
            single_reasons.append('该项目微服务数量较少')
            services_reasons_level.append('warning')
            services_reasons_count[9] += 1
            all_services_count[9] += 1

        services_tags[metric[0]] = ','.join(single_tags)
        services_reasons[metric[0]] = ','.join(single_reasons)
        services_levels[metric[0]] = ','.join(services_reasons_level)

    return services_tags, services_reasons, services_reasons_count, services_levels


def get_services_info(single_metric, services_len, all_services_count):
    all_percent = list()
    single_metric = np.array(single_metric)
    all_percent.append(_get_percent(single_metric[:, 1]))
    all_percent.append(_get_percent(single_metric[:, 2]))
    all_percent.append(_get_percent(single_metric[:, 3]))
    all_percent.append(_get_percent(single_metric[:, 4]))
    all_percent.append(_get_percent(single_metric[:, 5]))
    all_percent.append(_get_percent(single_metric[:, 6]))
    all_percent.append(_get_percent(single_metric[:, 7]))
    all_percent.append(_get_percent(single_metric[:, 8]))
    all_percent.append(_get_percent(single_metric[:, 9]))
    tags, reasons, reasons_count, services_levels = get_tags_and_reasons(single_metric, all_percent, services_len,
                                                                         all_services_count)

    return tags, reasons, reasons_count, services_levels


def _get_level(value, itype):
    level_list = list()
    [value_q1, value_q2, value_q3, value_ulim, value_llim] = _get_percent(value)
    for item in value:
        if itype == 'IFN' or itype == 'ifn' or itype == 'ECF' or itype == 'ecf':
            if item > value_q3:
                level_list.append('D')
            elif item > value_q2:
                level_list.append('C')
            elif item > value_q1:
                level_list.append('B')
            else:
                level_list.append('A')
        else:
            if item > value_q3:
                level_list.append('A')
            elif item > value_q2:
                level_list.append('B')
            elif item > value_q1:
                level_list.append('C')
            else:
                level_list.append('D')
    return level_list


def _get_percent(value):
    # 使用箱线图计算行数、评分的1/4、1/2、3/4数
    [value_q1, value_q2, value_q3, value_ulim, value_llim] = get_percent(value)

    return [value_q1, value_q2, value_q3, value_ulim, value_llim]


# def compete_all_score(owner, weight, version, type_names):
#     # 如果已经计算过综合评分就无需再次计算
#     projects_data = query_data_from_project(owner)
#     for project in projects_data:
#         # print(project.Project)
#         if project.score != 0:
#             continue
#         [services_name, index_matrix] = _get_index_matrix(type_names, project.projectname, version, project.plannum,
#                                                           owner)
#         [normalized_result, score_result] = _get_score(index_matrix, weight, type_names, project.projectname, version,
#                                                        project.plannum, owner)
#         # 将服务名、指标值和综合评分读入csv文件中
#         _output_to_csv(services_name, type_names, normalized_result, score_result, project.projectname, version, owner)


def compete_one_score(owner, weight, version, type_names, project_name):
    plan_num = EvaluatorAvgData.objects.filter(projectname=project_name, version=version, owner=owner).first().plannum
    [services_name, index_matrix] = _get_index_matrix(type_names, project_name, version, plan_num,
                                                      owner)
    [normalized_result, score_result] = _get_score(index_matrix, weight, type_names, project_name, version,
                                                   plan_num, owner)
    # 将服务名、指标值和综合评分读入csv文件中
    _output_to_csv(services_name, type_names, normalized_result, score_result, project_name, version, owner)


# 拼接指标矩阵:根据用户传进来的指标合集，拼接出指标矩阵
def _get_index_matrix(type_names, project_name, version, plan_num, owner):
    services_name = []
    project_detail_data = EvaluatorDetailData.objects.filter(itype=type_names[0], projectname=project_name, owner=owner,
                                                           plannum=plan_num, version=version)
    index_matrix = [['' for col in range(len(type_names))] for row in range(len(project_detail_data))]

    if len(type_names):
        for index1 in range(0, len(type_names)):
            # 根据传入的指标名字、项目名和用户名查库，拿出所有的指标数据拼接矩阵和服务名数组
            project_detail_data = EvaluatorDetailData.objects.filter(itype=type_names[index1], projectname=project_name,
                                                                   owner=owner, plannum=plan_num,
                                                                   version=version).order_by('servicename')
            # print('len(projectDetailData)', len(project_detail_data))
            for index2 in range(0, len(project_detail_data)):
                if project_detail_data[index2].servicename not in services_name:
                    services_name.append(project_detail_data[index2].servicename)
                index_matrix[index2][index1] = float(project_detail_data[index2].value)

    return [services_name, index_matrix]


# 传入指标矩阵和权重数组，计算最后的综合评分
def _get_score(index_matrix, weight, type_names, project_name, version, plan_num, owner):
    # max_feature：越大越好；min_feature:越小越好
    max_feature = {'chm', 'chd', 'icf', 'scoh', 'ccoh'}
    min_feature = {'ifn', 'rei', 'idd', 'odd', 'ecf', 'scop', 'ccop'}
    normalized_result = [['' for col in range(len(type_names))] for row in range(len(index_matrix))]

    # axis为0时求每列最值，为1时求每行最值
    max = np.amax(index_matrix, axis=0)
    min = np.amin(index_matrix, axis=0)

    # 求出归一化指标值和最终的综合评分
    for index1 in range(0, len(index_matrix)):
        for index2 in range(0, len(index_matrix[index1])):
            # 最大最小值相等时，即所有微服务在这个指标表现值一样
            # if max[index2] - min[index2] == 0:
            #     normalized_result[index1][index2] = 0
            # else:
            # 遗留问题：对于整组数据全相等的不能简单处理为结果为0
            if type_names[index2] in min_feature:
                if max[index2] - min[index2] == 0:
                    # 一般情况下出现这种现象的情况：所有ifn为0或者1、所有scop全为0
                    normalized_result[index1][index2] = 1
                    continue
                # 数据标准化归一化
                normalized_result[index1][index2] = float(
                    format((max[index2] - index_matrix[index1][index2]) / (max[index2] - min[index2]), '.4f'))
            if type_names[index2] in max_feature:
                if max[index2] - min[index2] == 0:
                    # 若其中指标取值全为1，那么最后评分应该为1
                    if max[index2] == 1:
                        normalized_result[index1][index2] = 1
                    elif max[index2] == 0:
                        normalized_result[index1][index2] = 0
                    else:
                        normalized_result[index1][index2] = max[index2]
                    continue
                normalized_result[index1][index2] = float(
                    format((index_matrix[index1][index2] - min[index2]) / (max[index2] - min[index2]), '.4f'))

    # 求最终评分数组
    score_result = np.dot(normalized_result, weight)
    # 给予每个微服务相同的权重，并将最终结果存入数据库
    score = sum(score_result) / len(score_result)
    EvaluatorAvgData.objects.filter(projectname=project_name, owner=owner, version=version, plannum=plan_num).update(
        score=format(score, '.4f'))
    return [normalized_result, score_result]


def _output_to_csv(services_name, type_names, normalized_result, score_result, project_name, version, owner):
    file_path = '.\\evaluator\\data\\UploadData\\' + owner + '\\' + project_name + '\\' + version + '\\'
    # 判断这个路径是否存在，如果不存在则创建该路径
    if os.path.exists(file_path) is not True:
        os.makedirs(file_path)
    file_path = os.path.join(file_path, 'output.csv')
    f = open(file_path, "w", encoding='utf-8')
    for index1 in range(0, len(services_name)):
        f.write(services_name[index1] + ' ')
        for index2 in range(0, len(type_names)):
            f.write(str(normalized_result[index1][index2]) + ' ')
        f.write(str(score_result[index1]))
        f.write('\n')
    f.close()
