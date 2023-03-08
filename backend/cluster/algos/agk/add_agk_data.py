import json
# from project.serializers import ClusterDatasSerializer


def add_agk_data(project_name, json_path, algo_name):
    pass
#     project = query_project_by_name(project_name)
#     serializer = ClusterDatasSerializer(
#         data={'name': 'root', 'cluster': 0, 'relation': json.dumps({}), 'project': project.index,
#               'cluster_algo': algo_name})
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     parent_pk = serializer.data['id']
#     jsonCluster = main(project_name, json_path, algo_name)
#     # 整理聚类结果，将其入库
#     cluster_data = deal_cluster_data(jsonCluster, parent_pk, project.index, algo_name)
#     for selector in cluster_data:
#         serializer = ClusterDatasSerializer(data=selector)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # serializer = ClusterDatasSerializer(data=selector[1:], many=True)
#         # serializer.is_valid(raise_exception=True)
#         # serializer.save()


def deal_cluster_data(jsonCluster, parent_pk, project_id, algo_name):
    result_list = list()
    index = parent_pk + 1
    parent_cluster = 0
    cluster_root_pk = parent_pk
    for cluster in jsonCluster['data']:
        df_temp = {'id': index, 'cluster': parent_cluster + 1, 'name': cluster['name'], 'parent_node': cluster_root_pk,
                   'relation': json.dumps({"Call": {"delete": 11}, "Modify": {"delete": 3}, "Override": {"delete": 4}, "Set": {"delete": 6}, "Typed": {"delete": 1}, "UseVar": {"delete": 19}, "bindVar": {"delete": 1}}),
                   'project': project_id, 'color': '#247ba0', 'cluster_algo': algo_name}
        result_list.append(df_temp)
        cluster_root_pk = index
        index += 1
        parent_cluster += 1
        for child in cluster['children']:
            df_temp = {'id': index, 'cluster': parent_cluster + 1, 'name': child['name'],
                       'parent_node': cluster_root_pk,
                       'relation': json.dumps({"Call": {"delete": 11}, "Modify": {"delete": 3}, "Override": {"delete": 4}, "Set": {"delete": 6}, "Typed": {"delete": 1}, "UseVar": {"delete": 19}, "bindVar": {"delete": 1}}),
                       'project': project_id,
                       'value': child['value'],
                       'color': '#70c1b3', 'cluster_algo': algo_name}
            result_list.append(df_temp)
            index += 1
    return result_list
