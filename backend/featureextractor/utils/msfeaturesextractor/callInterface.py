import requests
import csv
import os

PROJECTMESSAGE_NEW_V4 = 'C:\\Users\\20465\\Desktop\\data\\projects.csv'
APIFILE_URL = 'http://localhost:8080/getAPIFile'
SCFILE_URL = 'http://localhost:8080/getSCFile'
COMMITFILE_URL = 'http://localhost:8080/getVersionCmtFile'
STRUCTUREFILE_URL = 'http://localhost:8080/getStructdepFile'
GIT_COMMAND = 'git log  --pretty=format:"commit %H(%ad)%nauthor:%an%ndescription:%s"  --date=format:"%Y-%m-%d %H:%M:%S" --numstat  --name-status  --reverse  >./master.txt'


if __name__ == '__main__':
    os.chdir('D:\codes\Launcher3')
    os.system(GIT_COMMAND)

# def get_projects_url(type):
#     projects_services_url = {}
#     projects_url = []
#     apitype = []
#     projects_name = []
#     with open(PROJECTMESSAGE_NEW_V4, 'r') as f:
#         reader = csv.reader(f)
#         header = next(reader)
#         for line in reader:
#             projects_url.append(line[3])
#             if type == 'sc':
#                 projects_services_url[line[4]] = line[5]
#             elif type == 'api':
#                 projects_services_url[line[4]] = line[6]
#                 apitype.append(line[7])
#             elif type == 'class':
#                 projects_name.append(line[0])
#     return projects_services_url, projects_url, apitype, projects_name
#
#
# def get_api_file():
#     servicenames_apis_url, projects_url, apitype, projects_name = get_projects_url('api')
#     r = requests.post(APIFILE_URL, json = {'servicenames_apis_url': servicenames_apis_url, 'projects_url': projects_url, 'type': apitype})
#     if r.text == 'OK':
#         print('成功')
#
#
# def get_sc_file():
#     servicenames_services_url, projects_url, apitype, projects_name = get_projects_url('sc')
#     print(servicenames_services_url)
#     r = requests.post(SCFILE_URL, json = {'servicenames_services_url': servicenames_services_url, 'projects_url': projects_url})
#     if r.text == 'OK':
#         print('成功')
#     # for url in projects_services_url:
#     #     r = requests.get(SCFILE_URL, params = {'projectpath': url, 'servicespath': projects_services_url[url]})
#     #     if r.text == 'OK':
#     #         print('成功')
#
#
# def get_commitfile():
#     # projects_services_url, projects_url, apitype, projects_name = get_projects_url('cmt')
#     r = requests.post(COMMITFILE_URL, json={'urls': 'C:\\Users\\20465\\Desktop\\data\\Android\\base'})
#     if r.text == 'OK':
#         print('成功')
#     # for url in projects_services_url:
#     #     # 获取该项目在git上的提交记录
#     #     get_master_file(url)
#     #     r = requests.get(COMMITFILE_URL, json = {'urls': projects_url})
#     #     if r.text == 'OK':
#     #         print('成功')
#
#
# def get_structdep_file():
#     servicenames_paths_url, projects_url, apitype, projects_name = get_projects_url('class')
#     r = requests.post(STRUCTUREFILE_URL, json = {'urls': projects_url, 'names': projects_name})
#     print(r.text)
#     if r.text == 'OK':
#         print('成功')
#
#
# def get_master_file():
#     servicenames_paths_url, projects_url, apitype, projects_name = get_projects_url('master')
#     for url in projects_url:
#         print(url)
#         # 切换目录到当前项目下
#         os.chdir(url)
#         if os.path.exists('./master.txt'):
#             os.remove('./master.txt')
#         os.system(GIT_COMMAND)
#
#
# if __name__ == '__main__':
#     # get_sc_file()
#     # get_api_file()
#     # get_master_file()
#     get_commitfile()
#     # get_structdep_file()
