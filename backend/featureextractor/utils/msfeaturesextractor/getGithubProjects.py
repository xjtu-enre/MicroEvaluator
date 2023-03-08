#coding=utf-8 

import requests
import json
import csv
import os
# from git.repo import Repo

# from evaluator.const import project_const
PROJECTMESSAGE = 'C:\\Users\\20465\\Desktop\\data\\projectMessage.csv'
GITHUB_URL = 'https://api.github.com/search/repositories'
HEADERS = {"Authorization":"token "+"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"}
DOWNLOAD_PATH = 'C:\\Users\\20465\\Desktop\\data\\gitcodes\\'

def getProjectsMessage():
    projectMessage = []
    # https://docs.github.com/en/github/searching-for-information-on-github/searching-on-github/searching-code
    # q：搜索限定词；sort：排序关键词；order：升序或降序；per_page：每页结果个数，最大为100；page：默认第1页
    # 按文件大小搜索：function size:>10000 language:python==>匹配用 Python 编写的大于 10 KB 的文件中带有“function”一词的代码
    # params = {"q": "microservice+language:java", "sort": "stars", "order":"desc", "per_page": 100, "page": 4}
    # params = {"q": "coolstore-microservice", "sort": "stars", "order":"desc", "per_page": 100, "page": 4}
    # r = requests.get(project_const.GIT_SEARCH_URL, params = params, headers = project_const.GITHUB_HEADER)
    # r = requests.get(GITHUB_URL, params=params, headers=HEADERS)
    r = requests.get('https://github.com/junit-team/junit4', headers=HEADERS)
    if r.status_code != 200:
        print('连接不成功！') 
        return
    json_list = json.loads(r.text)
    print(json_list['total_count'])
    # pagenum = math.ceil(json_list['total_count'] / 100)
    projectMessage.extend(json_list['items'])
    # for index in range(1, 1):
    #     params = {"q": "microservice+language:java", "sort": "stars", "order":"desc", "per_page": 2, "page": index}
    #     r = requests.get('https://api.github.com/search/repositories', params = params, headers = HEADERS)
    #     json_list = json.loads(r.text)
    #     projectMessage.extend(json_list['items'])
    return projectMessage


def write2CSV(projectsMessage):
    # UTF-8以字节为编码单元，它的字节顺序在所有系统中都是一様的，没有字节序的问题，因此它实际上并不需要BOM(“ByteOrder Mark”)。但是UTF-8 with BOM即utf-8-sig需要提供BOM（"ByteOrder Mark"）。
    with open(PROJECTMESSAGE, 'w', encoding='utf_8_sig', newline='') as f:
        csv_write = csv.writer(f)
        csv_head = ["projectName", "description", "giturl", "downloadurl", "servicesname", "language", "loc", "sumloc", "star", "fork", "tags", "createTime", "lastupdateTime"]
        csv_write.writerow(csv_head)
        # 解决项目重名问题
        projectname = {}
        for item in projectsMessage:
             # 获取项目tags信息
            tagsurl = item['tags_url']
            r = requests.get(tagsurl, headers = HEADERS)
            tags_json_list = json.loads(r.text)
            tags = []
            # if len(tags_json_list) == 0:
            #     continue
            for tag in tags_json_list:
                tags.append(tag['name']) 

            # 获取项目语言及行数信息
            languageurl = item['languages_url']
            r = requests.get(languageurl, headers = HEADERS)
            language_json_list = json.loads(r.text)
            language = []
            loc = []
            sumloc = 0
            for key in language_json_list:
                language.append(key) 
                loc.append(str(language_json_list[key]))
                sumloc = sumloc + language_json_list[key]
            
            #创建本地路径用来放置远程仓库下载的代码
            name = item['name']
            project_name = ''
            if name.lower() in projectname:
                count = projectname[name.lower()] + 1
                download_path = DOWNLOAD_PATH + name.lower() + str(count)
                project_name = name.lower() + str(count)
            else:
                projectname[name] = 0
                download_path = DOWNLOAD_PATH + name.lower()
                project_name = name.lower()

            if not os.path.exists(download_path):
                os.mkdir(download_path)

            item_mess = [project_name, item['description'], item['html_url'], download_path, '', ';'.join(language), ';'.join(loc), sumloc, item['watchers'], item['forks'], ';'.join(tags), item['created_at'], item['updated_at']]
            csv_write.writerow(item_mess)
    f.close()


def main():
    projectsMessage= getProjectsMessage()
    # print(len(projectsMessage))
    # write2CSV(projectsMessage)


if __name__ == '__main__':
    main()
