import os

from featureextractor.utils.commitextractor.gitlogprocessor import gitlog
from featureextractor.utils.commitextractor.getnode import get_nodefile
from featureextractor.utils.commitextractor.cproness import changeproness


def get_commit_info(url, version):
    # 切换到项目目录下(主要是为了切换项目的不同分支)
    os.chdir(url)
    os.system("git checkout -f " + version)
    java_file_path = gitlog(url)
    node_url = url + "-node.csv"
    outfile = url + '/mc/' + 'count.csv'
    get_nodefile(url, node_url)
    changeproness(node_url, java_file_path, outfile)
    return outfile


if __name__ == '__main__':
    get_commit_info('G:\dataset1\AOSP\projects\LineageOS', 'lineage-17.1')

