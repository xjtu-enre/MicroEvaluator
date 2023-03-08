import os
import re
import pandas as pd
import numpy as np
from cluster.utils.dataStructure import ProjectFilesTrieTree
from cluster.serializers import *


def count_standardization(string):
    names = string.split('/')
    if '.java' in names[len(names) - 1]:
        names[len(names) - 1] = names[len(names) - 1].split('.')[0]
        return '.'.join(names[1:len(names)])
    return '.'.join(names[1:len(names)])


def get_color_by_changeLoc(number):
    color_list = ['#247ba0', '#70c1b3', '#b2dbbf', '#f3ffbd', '#ff1654']
    if 0 <= number <= 50:
        index = 0
    elif 50 < number <= 100:
        index = 1
    elif 100 < number <= 500:
        index = 2
    elif 500 < number <= 1000:
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


def get_relation_df(json_dict, meta, operator):
    df = pd.DataFrame(json_dict)
    df['meta'] = meta
    df['operator'] = operator
    return df


# def relation_standardization(string):
#     if '/' in string and '.java' in string:
#     # string = string.replace('.', '/')
#     # patterns = ['([a-z]*/)*([A-Z].*?/)', '([a-z]*/)*([A-Z].*)']
#     # results = list(
#     #     filter(lambda x: x is not None,
#     #            map(lambda y: re.search(y, string), patterns)))
#     # result = '' if len(results) == 0 else results[0].group() if len(
#     #     results) == 1 else results[0].group()[:-1]
#     return result


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


def post_visualization_data(version_project_id, project_name, version):
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    serializers = CatelogueDatasSerializer(
        data={
            'name':
                project_name,
            'version_project':
                version_project_id
        })
    serializers.is_valid(raise_exception=True)
    serializers.save()
    parent_pk = serializers.data['id']
    serializer = CatelogueTreeMapDatasSerializer(
        data={
            'name': 'root',
            'version_project': version_project_id,
            'value': [],
            'relation': json.dumps({})
        })
    serializer.is_valid(raise_exception=True)
    serializer.save()
    root_pk = serializer.data['id']

    structure_file = './featureextractor/data/' + project_name + '/' + version + '/' + project_name + '-out.json'
    count_file = './featureextractor/data/' + project_name + '/count.csv'
    relation_file = './featureextractor/data/' + project_name + '/relation.json'

    with open(structure_file, 'r', encoding='utf-8') as f:
        json_object = json.load(f, strict=False)
    # 读取统计文件
    df_count = pd.read_csv(count_file)
    df_count.rename(columns={
        'filename': 'name',
        'changeloc': 'changeLoc'
    },
        inplace=True)
    df_project = pd.DataFrame({'name': get_file_name(json_object['variables'])})
    df_merge = pd.merge(df_project,
                        df_count.loc[:, ['name', 'changeLoc']],
                        on='name')
    df_merge['color'] = df_merge['changeLoc'].apply(
        lambda x: get_color_by_changeLoc(x))
    df_merge['catelogue_type'] = 2
    df_merge['parent_catelogue'] = parent_pk
    df_merge['version_project'] = version_project_id
    df_merge['value'] = df_merge['changeLoc'].apply(
        lambda x: get_value_by_changeLoc(x))

    # # 用于生成依赖图
    # df_cells = pd.DataFrame([{
    #     'id': selector[0],
    #     'source': selector[1]['src'],
    #     'target': selector[1]['dest'],
    #     'values': json.dumps(selector[1]['values'])
    # } for selector in enumerate(json_object['cells'])])
    # df_cells['version_project'] = version_project_id
    # 读取依赖变更文件
    df_relation = get_relation_result_df(relation_file)
    # df_drop = df_merge.append(df_relation).drop_duplicates(['name'],
    #                                                        keep=False)
    # df_drop.drop(df_drop[np.isnan(df_drop['changeLoc'])].index, inplace=True)
    df_result = pd.merge(df_merge, df_relation, on='name')
    df_result.sort_index(ignore_index=True, inplace=True)
    df_result.fillna(json.dumps(dict()), inplace=True)
    df_result['catelogue_type'] = df_result['catelogue_type'].astype(int)
    df_result['parent_catelogue'] = df_result['parent_catelogue'].astype(int)
    df_result['version_project'] = df_result['version_project'].astype(int)
    tree_data_list = post_catelogueTreeMapDatas_data(df_result, root_pk, version_project_id)

    serializers = SubCatelogueDatasSerializer(data=df_result.to_dict(orient='records'),
                                              many=True)
    serializers.is_valid(raise_exception=True)
    serializers.save()
    for selector in tree_data_list:
        serializers = CatelogueTreeMapDatasSerializer(
            data=selector, many=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()


def post_catelogueTreeMapDatas_data(origin_df, root_id, version_project_id):
    tree = ProjectFilesTrieTree(origin_df.max()['changeLoc'], root_id, version_project_id)
    origin_df.apply(lambda x: tree.insert(x['name'].split('/'), x['changeLoc']), axis=1)
    df = pd.DataFrame(tree.getRoot())
    df.drop(index=df.loc[(df['name'] == 'root')].index, inplace=True)
    origin_df['qualifiedName'] = origin_df['name']
    origin_df = origin_df.loc[:, ['qualifiedName', 'color', 'relation']]
    df_drop = df[df['end'] == False]
    df_merge = pd.merge(df, origin_df, on='qualifiedName')
    df_result = df_drop.append(df_merge)
    df_result['color'].fillna('C0C0C0', inplace=True)
    df_result['id'] = df_result['id'].astype(int)
    df_result['relation'].fillna(json.dumps(dict()), inplace=True)
    df_result['version_project'] = version_project_id
    df_result.sort_values(by=['catelogue_type', 'id'], inplace=True)
    groupby_list = [selector[1].to_dict(orient='records') for selector in list(df_result.groupby(['catelogue_type']))]
    return groupby_list


def get_file_name(variables):
    result = list()
    for v in variables:
        if not v['external'] and 'File' in v['category']:
            result.append(v['File'])
    return list(set(result))
