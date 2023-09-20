import celery.app.control

from backend.celery import backend
from project.models import *
from featureextractor.utils.featureUtil import post_feature_files
from cluster.utils.visualizationUtil import post_visualization_data
from cluster.utils.sectionUtil import post_section_data
from cluster.utils.clusterUtil import post_cluster_data
from evaluator.utils.evaluatorUtil import post_evaluator_data
# from celery.task.control import revoke

@backend.task(bind=True, name='tasks.storeData')
def storeData(self, version_info, project_name, url, ismicro):
    # taskid=self.request.id
    # revoke(taskid, terminate=True)
    # celery.app.control.revoke(taskid, terminate=True)
    progress = 0
    print("begin to post_feature_files...")
    # for v_pro in version_info:
    #     print('v: ')
    #     print(v_pro)#增加输出语句，这段代码有问题,ver示例分号连接多版本;
    post_feature_files(project_name, version_info, url, ismicro)
    progress += 25
    print('proecss', progress)
    storeData.update_state(state='PROGRESS', meta={'progress': progress})
    print("begin to post_evaluator_data...")
    post_evaluator_data(project_name, version_info, ismicro)
    progress += 25
    print('proecss', progress)
    storeData.update_state(state='PROGRESS', meta={'progress': progress})
    incre_progress = 25 / len(version_info)
    print("begin to post_visualization_data...")
    # for v_data in version_info:
    verLen = len(version_info)
    post_visualization_data(version_info[verLen - 2]['id'], project_name, version_info[verLen - 2]['version'])
    progress += incre_progress
    print('proecss', progress)
    storeData.update_state(state='PROGRESS', meta={'progress': progress})
    # print("begin to post_section_data...")
    # post_section_data(21)
    # progress += 20
    # print('proecss', progress)
    # self.update_state(state='PROGRESS', meta={'progress': progress})
    print("begin to post_cluster_data...")
    # incre_progress = 25 / len(version_info)
    # for v_data in version_info:
    post_cluster_data(project_name, version_info[verLen - 2]['id'], version_info[verLen - 2]['version'], 'AGK')
    progress += incre_progress
    # print('proecss', progress)
    storeData.update_state(state='PROGRESS', meta={'progress': progress})


def check_task_process(task_id):
    task = storeData.AsyncResult(task_id)
    status = task.state
    print(status)
    print(task.result)

    progress = 0
    if status == 'SUCCESS':
        progress = 100
    elif status == 'FAILURE':
        progress = 0
    elif status == 'PROGRESS':
        progress = task.result['progress']
    return progress
