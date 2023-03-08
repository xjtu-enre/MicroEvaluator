import json
import os
import pandas as pd
from cluster.algos.agk.CommonFunction import mainMethod
from cluster.serializers import *


def post_cluster_data(project_name, version_project_id, version, cluster_algorithm):
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    structure_file = './featureextractor/data/' + project_name + '/' + version + '/' + project_name + '-out.json'
    count_file = './featureextractor/data/' + project_name + '/count.csv'
    relation_file = './featureextractor/data/' + project_name + '/relation.json'
    AssociationNetworkName = 'Construct'
    GraphEmbeddingAlgorithm = 'Node2Vec'
    # ClusterAlgorithm =
    ClusterNum = 6
    # json_cluster = dict()
    json_cluster = mainMethod(SoftwareName='NewForm' + project_name,
                             jsonFileName=structure_file,
                             AssociationNetworkName=AssociationNetworkName,
                             GraphEmbeddingAlgorithm=GraphEmbeddingAlgorithm,
                             ClusterAlgorithm=cluster_algorithm,
                             ClusterNum=ClusterNum)
    return add_agk_data(version_project_id, structure_file, count_file, relation_file, json_cluster, cluster_algorithm)


def add_agk_data(version_project_id, structure_file, count_file, relation_file, json_cluster, cluster_algorithm):
    serializer = ClusterDatasSerializer(
        data={'name': 'root', 'cluster': 0, 'relation': json.dumps({}), 'version_project': version_project_id,
              'cluster_algo': cluster_algorithm})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    root_pk = int(serializer.data['id'])
    # 整理聚类结果，将其入库
    return deal_cluster_data(json_cluster, structure_file, count_file, relation_file, root_pk, version_project_id, cluster_algorithm)


def deal_cluster_data(json_cluster, structure_file, count_file, relation_file, root_pk, version_project_id, algo_name):
    leaf_nodes = list()
    print(json_cluster)
    # cluster代表层级
    for cluster in json_cluster['data']:
        cluster_id = 1
        serializer = ClusterDatasSerializer(
            data={'name': cluster['name'], 'cluster': cluster_id, 'relation': json.dumps({}),
                  'version_project': version_project_id,
                  'cluster_algo': algo_name, 'parent_node': root_pk, 'color': '#247ba0'})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        parent_pk = int(serializer.data['id'])
        for child in cluster['children']:
            cluster_id = 2
            leaf_nodes.append([child['name'], cluster_id, parent_pk])
            # serializer = ClusterDatasSerializer(
            #     data={'name': child['name'], 'cluster': cluster_id, 'relation': json.dumps({}),
            #           'version_project': version_project_id,
            #           'cluster_algo': algo_name, 'parent_node': parent_pk, 'color': '#70c1b3', 'value': child['value']})
            # serializer.is_valid(raise_exception=True)
            # serializer.save()

    name_to_path = get_path(structure_file)
    leaf_nodes = pd.DataFrame(leaf_nodes, columns=['name', 'cluster', 'parent_node'])
    leaf_nodes['name'] = leaf_nodes['name'].apply(
        lambda x: get_file_path(x, name_to_path))
    # 对leaf_nodes的name列为空的数据进行筛选，加负号的原因是想删除符合条件的行，不写负号是筛选出符合条件的行
    leaf_nodes = leaf_nodes[-leaf_nodes.name.isin([''])]
    leaf_nodes['version_project'] = version_project_id
    leaf_nodes['cluster_algo'] = algo_name

    df_count = pd.read_csv(count_file)
    df_count.rename(columns={
        'filename': 'name',
        'changeloc': 'changeLoc'
    },
        inplace=True)
    df_merge = pd.merge(leaf_nodes,
                        df_count.loc[:, ['name', 'changeLoc']],
                        on='name')
    df_merge['color'] = df_merge['changeLoc'].apply(
        lambda x: get_color_by_changeLoc(x))
    df_merge['value'] = df_merge['changeLoc'].apply(
        lambda x: get_value_by_changeLoc(x))
    # 读取依赖变更文件
    df_relation = get_relation_result_df(relation_file)
    df_result = pd.merge(df_merge, df_relation, on='name')
    df_result.sort_index(ignore_index=True, inplace=True)
    df_result.fillna(json.dumps(dict()), inplace=True)
    serializers = ClusterDatasSerializer(data=df_result.to_dict(orient='records'),
                                              many=True)
    serializers.is_valid(raise_exception=True)
    serializers.save()

    return json_cluster['data']

def get_path(structure_file):
    with open(structure_file, 'r', encoding='utf-8') as f:
        json_object = json.load(f, strict=False)

    res = dict()
    for var in json_object['variables']:
        if not var['external'] and 'File' in var['category']:
            res[var['qualifiedName']] = var['File']

    return res

def get_file_path(name, name_to_path):
    return name_to_path[name] if name in name_to_path else ''

def get_color_by_changeLoc(number):
    color_list = ['#247ba0', '#70c1b3', '#b2dbbf', '#f3ffbd', '#ff1654']
    if 0 <= number <= 100:
        index = 0
    elif 100 < number <= 500:
        index = 1
    elif 500 < number <= 1000:
        index = 2
    elif 1000 < number <= 2000:
        index = 3
    else:
        index = 4
    return color_list[index]


def get_value_by_changeLoc(number, time=100):
    if 0 <= number <= 100:
        return 0.25 * time
    elif 100 < number <= 500:
        return 0.3 * time
    elif 500 < number <= 1000:
        return 0.4 * time
    elif 1000 < number <= 2000:
        return 0.6 * time
    else:
        return 0.8 * time


def get_relation_result_df(relation_file):
    with open(relation_file, 'r', encoding='utf-8') as f:
        relation_json_object = json.load(f, strict=False)
    relation_df_list = [
        get_relation_df(selector[1], item[0], selector[0])
        for item in list(relation_json_object.items())
        for selector in list(item[1].items())
    ]
    relation_df = pd.concat(relation_df_list)
    relation_df.sort_index(ignore_index=True, inplace=True)
    relation_df['name'] = relation_df['src']
    relation_filter_df = relation_df.loc[relation_df['name'].str.contains('/'),
                                         ['name', 'meta', 'operator']]
    groupby_name_list = list(relation_filter_df.groupby(['name']))
    groupby_meta_list = [{
        'name': item[0],
        'relation': list(item[1].groupby(['meta']))
    } for item in groupby_name_list]
    groupby_result_list = \
        [{'name': selector.get('name'),
          'relation': json.dumps(dict([(
              item[0], item[1].loc[:, ['meta', 'operator']].groupby(['operator']).count().to_dict().get('meta')) for
              item in selector.get('relation')]))} for selector in groupby_meta_list]
    return pd.DataFrame(groupby_result_list)

def get_relation_df(json_dict, meta, operator):
    df = pd.DataFrame(json_dict)
    df['meta'] = meta
    df['operator'] = operator
    return df
