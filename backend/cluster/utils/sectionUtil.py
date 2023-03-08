import os
import json
import pandas as pd
from cluster.utils.fileUtil import un_zip_sectionFile
from cluster.utils.dataStructure import SectionFilesTrieTree
from cluster import serializers


def post_section_data(version_project_id):
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    ori_file = './featureextractor/data/coupling-patterns.zip'
    contents = un_zip_sectionFile(ori_file)
    df = pd.DataFrame(contents)
    tree = SectionFilesTrieTree(1)
    df['qualifiedName'].apply(lambda x: tree.insert(x.split('/')))
    df_tree = pd.DataFrame(tree.getRoot())
    df_tree.drop(index=df_tree.loc[(df_tree['name'] == 'root')].index,
                 inplace=True)
    df_tree_drop = df_tree.loc[df_tree['end'] == False]
    df_tree_drop.rename({'name': 'file_name'}, axis=1, inplace=True)
    df_tree_drop['file_extension'] = 'folder'
    df_tree.drop(columns=['name'], inplace=True)
    df_merge = pd.merge(df, df_tree, on=['qualifiedName'])
    df_merge.sort_index(ignore_index=True, inplace=True)
    df_merge['number'] = df_merge.index
    df_merge['status'] = False
    df_node_list, df_edge_list = [], []
    for selector in enumerate(df_merge.to_dict(orient='records')):
        get_section_data(selector[1], df_node_list, df_edge_list)
        df_merge.at[selector[0], 'status'] = True
    df_nodes = pd.concat(df_node_list)
    df_temp = df_nodes.drop_duplicates(subset=['id', 'mode_type'],
                                       keep='first')
    df_temp = df_temp.groupby(['id'])['mode_type'].apply(
        lambda x: ','.join(x.values)).apply(lambda x: x.split(','))
    df_temp = pd.DataFrame([{
        '_id': item[0],
        'mode_type': item[1]
    } for item in df_temp.to_dict().items()])
    df_nodes.drop(
        ['isIntrusive', 'parameterTypes', 'rawType', 'maxTargetSdk'],
        axis=1,
        inplace=True)
    df_nodes.rename(columns={
        'id': '_id',
        'not_aosp': 'isHonor'
    },
        inplace=True)
    df_nodes['_global'] = df_nodes['global']
    df_nodes.drop(['global'], axis=1, inplace=True)
    df_nodes['modifiers'] = df_nodes['modifiers'].where(
        df_nodes['modifiers'].notnull(), 'default')
    df_nodes['modifiers'] = df_nodes['modifiers'].apply(lambda x: 'default'
    if x == '' else x)
    df_nodes = df_nodes.where(df_nodes.notnull(), None)
    df_nodes['version_project'] = version_project_id
    df_nodes.drop_duplicates(subset=['_id'], keep='first', inplace=True)
    df_nodes.drop('mode_type', axis=1, inplace=True)
    df_nodes = pd.merge(df_nodes, df_temp, on=['_id'], how='left')
    df_edges = pd.concat(df_edge_list)
    df_edges['version_project'] = version_project_id
    serializer = serializers.SectionNodesSerializer(
        data=df_nodes.to_dict(orient='records'), many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    serializer = serializers.SectionEdgesSerializer(
        data=df_edges.to_dict(orient='records'), many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()


def get_section_data(selector, df_node_list, df_edge_list):
    temp_list = [[], []]
    df_list = []
    temp = json.loads(selector['file'].file.getvalue())
    dict_list = temp['res']
    for items in dict_list:
        for item in items.items():
            if item[0] != 'values':
                temp_list[0].append(item[1])
            else:
                temp_list[1].append({
                    'source':
                        items['src']['id'],
                    'sourceFile':
                        items['src']['File'],
                    'sourcePackageName':
                        items['src']['packageName'],
                    'sourceIsHonor':
                        items['src']['not_aosp'],
                    'target':
                        items['dest']['id'],
                    'targetFile':
                        items['dest']['File'],
                    'targetPackageName':
                        items['dest']['packageName'],
                    'targetIsHonor':
                        items['dest']['not_aosp'],
                    'value':
                        list(items['values'].keys())[0]
                })
    for temp in temp_list:
        df = pd.DataFrame(temp)
        df['mode_type'] = selector['mode_type']
        df_list.append(df)
    df_node_list.append(df_list[0])
    df_edge_list.append(df_list[1])
