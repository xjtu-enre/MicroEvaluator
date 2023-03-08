from django.urls import include, path
from rest_framework import routers
from evaluator import views
from .utils.evaluatorUtil import post_evaluator_data


router = routers.DefaultRouter()
# router.register('projectdata', views.ProjectDataViewSet)
# router.register('moduledata', views.ModuleDataViewSet)

urlpatterns = [
    # path('test/', test.test),
    path('', include(router.urls)),
    path('projectdata/', views.get_all_metric_data, name='projectdata'),
    path('linedata/', views.get_line_data, name='linedata'),
    path('hotmapdata/', views.get_hotmap_data, name='hotmapdata'),
    path('metricdata/', views.get_metric_data, name='metricdata'),
    path('treedata/', views.get_tree_data, name='treedata'),
    path('cause/', views.get_cause_entities, name='cause'),
    # path('addData/', post_evaluator_data, name='addData')
    # 一般场景度量数据获取
    # path('getProjectData/', views.add_user_view, name='addUser'),
    # path('getHotMapData/', views.add_user_view, name='addUser'),

    # path('addUser/', views.add_user_view, name='addUser'),
    # path('login/', views.login_view, name='login'),
    # # path('get_metrics/', views.get_metrics, name='get_metrics'),
    # # 四个维度的数据获取
    # path('get_all_Data_functionality/', views.fun_view, name='get_all_Data_functionality'),
    # path('get_all_Data_evolvability/', views.e_view, name='get_all_Data_evolvability'),
    # path('get_all_Data_modularity/', views.m_view, name='get_all_Data_modularity'),
    # path('get_all_Data_InteractionComplexity/', views.ic_view, name='get_all_Data_InteractionComplexity'),
    # # 获取拆分方案结果用于画图
    # path('drawTree/', views.draw_view, name='drawTree'),
    # # 上传特征文件
    # path('uploadSixFiles/', views.upload_view, name='uploadSixFiles'),
    # # # 新建项目
    # # path('addProject/', views.add_project, name='addProject'),
    # # # 删除项目
    # # path('deleteProject/', views.del_project, name='deleteProject'),
    # # 获取报告（暂时不使用该功能）
    # # path('getReport/', views.get_report_view, name='getReport'),
    # # 获取该项目的综合评分
    # path('getData/', views.get_project_and_microservice_view, name='getData'),
    # # path('getSpreadAndFocus/', sf_measure.getSpreadAndFocus, name='getSpreadAndFocus'),
    # # 根据提交历史记录，获取一些度量信息
    # path('getCmtMeasurements/', views.measure_cmt_view, name='getCmtMeasurements'),
    # # 获取项目各版本信息
    # path('getHistoryData/', views.get_history_data_view, name='getHistoryData'),
    # path('getHotMapData/', views.get_hotmap_data, name='getHotMapData'),
    # # 上传文件结束后生成各指标数据
    # path('competeMetricData/', views.compete_metric_data_view, name='competeMetricData'),
    # # 批量导入项目文件上传
    # path('uploadBatchFile/', views.upload_batch_file_view, name='uploadBatchFile'),
    # # 删除批量导入文件
    # path('deleteBatchFile/', views.del_batch_file_view, name='deleteBatchFile'),
    # # 批量导入项目处理
    # path('batchImportProject/', views.batch_import_project_view, name='batchImportProject'),
    # path('getProjectData/', views.get_project_data, name='getProjectData')
    # 获取github上的信息
    # path('getGithubProjects/', getGithubProjects.main, name='getGithubProjects'),
]
