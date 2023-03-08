# from visualization.views import add_data
from django.http import HttpResponse
from evaluator.utils.evaluatorUtil import post_evaluator_data
from cluster.utils.clusterUtil import post_cluster_data
from evaluator.utils.datautil import *


def test(request):
    post_cluster_data('Launcher3', 30, 'android-10.0.0_r29', 'AGK')
    # json_list = load_json()
    # project_metric_data, module_list = get_project_data(json_list)
    # post_evaluator_data('Launcher3', 4, ['android-10.0.0_r2', 'android-10.0.0_r29'])
    # version_project_id = request.get('version_project_id')
    # project_name = request.get('project_name')
    # version = request.get('version')
    # post_evaluator_data('Launcher3', [{'version': 'android-10.0.0_r2', 'id': 1}, {'version': 'android-10.0.0_r29', 'id': 2}], '0')
    # 新建项目
    # add_project_data('Launcher3', r'C:\Users\20465\Desktop\data\Android\Launcher3', 'test', '', '', '', 'java', 'android-11.0.0_r2;android-12.0.0_r2', 'test', 'test')
    # 生成依赖文件
    # vers = gen_dep_by_java_jar(r'C:\Users\20465\Desktop\data\Android\Launcher3', 'Launcher3', 'android-11.0.0_r2;android-12.0.0_r2')
    # # 依据依赖文件生成图数据、聚类数据和度量数据
    # add_data('android-11.0.0_r2;android-12.0.0_r2', 'Launcher3')
    # 删除项目
    # delete_project('Launcher3', 'test')
    return HttpResponse('ok')
