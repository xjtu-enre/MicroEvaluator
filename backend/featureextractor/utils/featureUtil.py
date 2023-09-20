import os
import shutil
from featureextractor.utils.structure_extractor.structure_diff import get_json_file
from featureextractor.utils.structure_extractor.relation_diff import get_diff_relation
from featureextractor.utils.commitextractor.commit_info import get_commit_info

GIT_COMMAND = 'git log  --pretty=format:"commit %H(%ad)%nauthor:%an%ndescription:%s"  --date=format:"%Y-%m-%d %H:%M:%S" --numstat  --name-status  --reverse  >./master.txt'


def post_feature_files(project_name, version_info, url, ismicro):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # base_dir是右斜线\\，后面连接路径用的左斜线/
    dir = base_dir.split('\\')
    base_dir = '/'.join(dir)
    print('base_dir:' + base_dir)

    result_url = base_dir + '/data/' + project_name + '/'
    version_old = version_info[1]['version'] #多个版本之间用分号连接，
    version_new = version_info[0]['version']
    print('version_new:'+version_new)

    for v_pro in version_info:
        version = v_pro['version']
        print(version_info)
        print(v_pro)
        # 切换到项目目录下(主要是为了切换项目的不同分支)
        os.chdir(url)
        os.system("git checkout -f " + version)
        # 获取当前项目的提交记录
        os.system(GIT_COMMAND)
        # 切换回当前工作路径下（防止后面使用路径时找不到）
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # 获取结构依赖
        execute1 = "java -jar {} java {} {}".format(base_dir +
                                                    '/utils/structure_extractor/enre_java.jar', url,
                                                    project_name)
        os.system(execute1)
        # 获取历史依赖
        execute2 = "java -jar {} {}".format(base_dir +
                                            '/utils/commitextractor/commit.jar', url)
        os.system(execute2)
        if os.path.isdir(base_dir + '/' + project_name + '-enre-out'):
            if not os.path.exists(base_dir + '/data/' + project_name + '/' + version):
                os.makedirs(base_dir + '/data/' + project_name + '/' + version)
            shutil.move(base_dir + '/' + project_name + '-enre-out/' + project_name + '-out.json',
                        result_url + version)
            shutil.move(url + '/' + 'cmt.csv', result_url + version)
            shutil.rmtree(base_dir + '/' + project_name + '-enre-out')
    print('version list dependency and cmt finished')
    # 获取历史维护指标信息(基于最后一个版本)
    outfile = get_commit_info(url, version_new)
    # 切换回当前工作路径下（防止后面使用路径时找不到）
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    shutil.move(outfile, result_url)
    shutil.rmtree(url + '/mc')
    # 获取两个版本的实体diff（默认取当前最新版本）
    get_json_file(result_url + version_old + '/' + project_name + '-out.json',
                  result_url + version_new + '/' + project_name + '-out.json',
                  result_url + 'entities-out.json')
    # 获取两个版本的依赖diff（默认取当前最新版本）
    get_diff_relation(result_url + version_old + '/' + project_name + '-out.json',
                      result_url + version_new + '/' + project_name + '-out.json',
                      result_url + 'entities-out.json',
                      result_url + 'relation.json')
    print('get diff relation success')
