import os
import shutil
from project.models import *
from project.serializers import *
from backend.utils.response import APIResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet
from project.tasks import *

authentication_class_list = [SessionAuthentication, BasicAuthentication]


# 包含项目信息的增(单条增加)删(单条删除)查(查询所有)
class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            # 提取特征文件->存储可视化数据->存储聚类数据->存储度量数据
            version_projects = Version.objects.filter(project=serializer.data['id']).all()
            version_info = self.get_version_info(version_projects)
            task_id = storeData.delay(version_info, serializer.data['projectname'], serializer.data['url'], serializer.data['ismicro'])
            return APIResponse(HTTP_200_OK, 'success', str(task_id))
        except:
            print(serializer.data)
            return APIResponse(HTTP_204_NO_CONTENT, 'fail', serializer.data)

    def get_version_info(self, version_projects):
        ver_info = list()
        for ver in version_projects:
            ver_info.append({'id': ver.id, 'version': ver.version})

        return ver_info

    def destroy(self, request, *args, **kwargs):
        id = kwargs['pk']
        # TODO:暂时删除对应路径下所有文件，之后会将特征文件存到文件服务器上，此处便删除
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if os.path.exists(base_dir + '/featureextractor/data/' + self.get_object().projectname):
            shutil.rmtree(base_dir + '/featureextractor/data/' + self.get_object().projectname)
        Project.objects.filter(id=id).delete()
        return APIResponse(HTTP_204_NO_CONTENT, 'delete success')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse(HTTP_200_OK, 'list success', serializer.data)

    def retrieve(self, request, *args, **kwargs):
        params = kwargs['pk'].split('&')
        task_id = params[0]
        project_name = params[1]
        progress = check_task_process(task_id)
        if progress == 100:
            Project.objects.filter(projectname=project_name).update(process=100)
        return APIResponse(HTTP_200_OK, 'retrieve success', progress)


# 版本相关数据的查询
class VersionProjectViewSet(ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionProjectSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse(HTTP_200_OK, 'list success', serializer.data)

    def retrieve(self, request, *args, **kwargs):
        project_id = kwargs['pk']
        versions = Version.objects.filter(project=project_id).all()
        serializer = self.get_serializer(versions, many=True)
        return APIResponse(HTTP_200_OK, 'retrieve success', serializer.data)


def test(request):
    storeData('lineage-16.0;lineage-17.1', 'lineage', 'G:\dataset1\AOSP\projects\LineageOS', 0)
