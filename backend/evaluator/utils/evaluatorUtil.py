import os

import requests

from evaluator.generalevaluator.function_file import *
from evaluator.generalevaluator.detect_algo.detect_root_cause import analyse_data
from project.models import *


def post_evaluator_data(project_name, version_info, ismicro):
    # def post_evaluator_data():
    #     project_name = 'leetcode'
    #     version_info = [{'version': 'v1.0', 'id': 112}, {'version': 'v1.2', 'id': 113}]
    #     ismicro = 0
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    project_dic = dict()
    vers = list()
    for ver_pro in version_info:
        v_id = ver_pro['id']
        version = ver_pro['version']
        vers.append(version)
        cmt_path = './featureextractor/data/' + project_name + '/' + version + '/cmt.csv'
        if ismicro == 1:
            api_path = './featureextractor/data/' + project_name + '/' + version + '/api.csv'
            sc_path = './featureextractor/data/' + project_name + '/' + version + '/sc.csv'
            structdep_path = './featureextractor/data/' + project_name + '/' + version + '/structdep.csv'
            concerndep_path = './featureextractor/data/' + project_name + '/' + version + '/concerndep.csv'
        else:
            dep_path = './featureextractor/data/' + project_name + '/' + version + '/' + project_name + '-out.json'
            measure_package_metrics(dep_path, cmt_path,
                                    './featureextractor/data/' + project_name + '/' + version + '/', v_id, version,
                                    project_dic, project_name)
    write_result_to_json('./featureextractor/data/' + project_name + '/measure_result.json', project_dic)

    # 最新两个版本求diff，用来画热力图
    compare_diff('./featureextractor/data/' + project_name + '/' + vers[0],vers[0],
                 './featureextractor/data/' + project_name + '/' + vers[1],vers[1], dict(),
                 './featureextractor/data/' + project_name)
    # # 根因定位
    # analyse_data('./featureextractor/data/diffResult', './featureextractor/data/' + project_name, 'notaosp')

