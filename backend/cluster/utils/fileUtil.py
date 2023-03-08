import os
import pandas as pd
import re
import zipfile
from django.conf import settings
from django.core.files.base import ContentFile


def un_zip_projectFile(file, file_name):
    sub_folder_dict = dict([(item, '{}/{}/'.format(file_name, item))
                            for item in settings.PROJECTFILE_SUB_FOLDER])
    zip_file = zipfile.ZipFile(file)
    name_list = list(
        filter(lambda x: contain(x, list(sub_folder_dict.values())),
               zip_file.namelist()))
    df = pd.DataFrame([{'name': name} for name in name_list])
    df['file'] = df['name'].apply(
        lambda x: ContentFile(zip_file.read(x), name=x))
    df['file_name'] = df['name'].apply(
        lambda x: re.findall('({}/)(.*/)(.*)'.format(file_name), x)[0][2])
    df = df[~df['file_name'].isin(['.DS_Store'])]
    df['sub_folder'] = df['name'].apply(
        lambda x: re.findall('({}/)(.*)(/.*)'.format(file_name), x)[0][1])
    zip_file.close()
    groupby_list = list(df[['file_name', 'file']].groupby(df['sub_folder']))
    groupby_list = dict([(selector[0], selector[1].to_dict(orient='records'))
                         for selector in groupby_list])
    return groupby_list


def un_zip_sectionFile(file):
    zip_file = zipfile.ZipFile(file)
    df = pd.DataFrame(
        [{'name': name} for name in zip_file.namelist() if name.find('.') != -1 and bool(re.search(r'\d', name))])
    df['file'] = df['name'].apply(lambda x: ContentFile(zip_file.read(x), name=x))
    df['file_name'] = df['name'].apply(lambda x: re.findall('/([0-9]+)/', x)[0])
    df['file_extension'] = df['name'].apply(lambda x: os.path.splitext(x)[-1][1:])
    df['mode_type'] = df['name'].apply(lambda x: re.findall('/(.*)/[0-9]+/', x)[0])
    df['name'] = df['name'].apply(lambda x: re.findall('(.*/[0-9]+)', x)[0])
    df.rename({'name': 'qualifiedName'}, axis=1, inplace=True)
    groupby_list = list(df.groupby(df['mode_type']))
    for selector in groupby_list:
        selector[1]['sort'] = selector[1]['file_name'].astype(int)
        selector[1].sort_values(by=['sort'], ascending=True, inplace=True)
        selector[1].drop(columns=['sort'], inplace=True)
    df = pd.concat([selector[1] for selector in groupby_list])
    zip_file.close()
    return df.to_dict(orient='records')


def contain(name, sub_folder_list):
    boolList = [
        name.startswith(item) & (name != item) for item in sub_folder_list
    ]
    return True in boolList
