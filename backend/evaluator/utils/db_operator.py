import pandas as pd
import numpy as np
from evaluator.utils import common
from evaluator.serializers import *


def save_project_to_db(module_data, version_id, module_dic, project_dic):
    result = list()
    for item in module_data:
        temp = [item[0] - item[1]]
        temp.extend(item[2: 9: 1])
        result.append(temp)
    tmp_pro = np.around(np.array(result).mean(axis=0).tolist(), 4)
    # project_df = pd.DataFrame(data={
    #     'metric': common.PROJECT_METRICS,
    #     'value': tmp_pro
    # }, columns=['metric', 'value'])
    # project_df['version'] = version_id
    # TODO:根据项目级的评分结果计算均分入库(project级:每次查看时都是动态更新的)

    # for data in project_df.to_dict(orient='records'):
    #     serializer = ProjectDataSerializer(data=data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()

    project_metric = dict(zip(common.PROJECT_METRICS, tmp_pro))
    project_metric['modules'] = module_dic
    project_dic[version_id] = project_metric
