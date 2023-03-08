from backend.utils.response import APIResponse
from rest_framework.filters import BaseFilterBackend
from cluster.serializers import *
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet
from django.db.models import Q
from cluster.utils.clusterUtil import *
from django.http import JsonResponse
import json

#
# class ProjectFilesFilter(BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         is_delete = False if request.query_params.get('is_delete') == 'false' else True
#         if request.query_params.get('parent_file_id') is None:
#             return queryset.filter(is_delete=is_delete).exclude(parent_file__isnull=False)
#         parent_file_id = int(request.query_params.get('parent_file_id'))
#         return queryset.filter(Q(is_delete=is_delete) & Q(parent_file=parent_file_id))


# # 项目文件和切面文件共同父类
# class FilesViewSet(GenericViewSet):
#     def uploadZip(self, request, *args, **kwargs):
#         file = request.FILES.get('file')
#         file_extension = re.findall('(?<=/).*$', file.content_type)[0]
#         file_name = file.name.replace('.{}'.format(file_extension), '')
#         data = {
#             'file': file,
#             'file_extension': re.findall('(?<=/).*$', file.content_type)[0],
#             'file_name': file_name
#         }
#         serializer = self.get_serializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         url = serializer.data['file']
#         ori_file = serializer.data['id']
#         return data, ori_file, url


class CatelogueDatasViewSet(GenericViewSet):
    queryset = CatelogueData.objects.all()
    serializer_class = CatelogueDatasSerializer

    # filter_visualizations = (DjangoFiltervisualization, filters.SearchFilter)
    # filter_fields = ['catelogue_type']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse(HTTP_200_OK, 'list success', serializer.data)


class CatelogueTreeMapDatasFilter():
    def filter_queryset(self, request, queryset, view):
        structure_file = int(request.query_params.get('structure_file'))
        return queryset.filter(Q(catelogue_type=1) & Q(structure_file_id=structure_file))


class CatelogueTreeMapDatasViewSet(GenericViewSet):
    queryset = TreeMapData.objects.all()
    serializer_class_list = [CatelogueTreeMapDatasWriteRootSerializer,
                             CatelogueTreeMapDatasWritePackageSerializer,
                             CatelogueTreeMapDatasWriteFileSerializer]
    filter_visualizations = [CatelogueTreeMapDatasFilter]

    def get_serializer_class_from_list(self, item):
        type_num = item.catelogue_type
        end = item.end
        if type_num == 1:
            return self.serializer_class_list[0](item)
        else:
            if end:
                return self.serializer_class_list[2](item)
            else:
                return self.serializer_class_list[1](item)

    def serialize_tree(self, queryset):
        for obj in queryset:
            data = self.get_serializer_class_from_list(obj).data
            if not obj.end:
                data['children'] = self.serialize_tree(obj.children.all())
            yield data

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.serialize_tree(queryset)
        return APIResponse(HTTP_200_OK, 'list success', data)


# class SectionFilesFilter(BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         is_delete = False if request.query_params.get('is_delete') == 'false' else True
#         return queryset.filter(Q(section_type=1) & Q(is_delete=is_delete))


# class SectionNodesViewSet(GenericViewSet):
#     queryset = SectionNodes.objects.all()
#     serializer_class = SectionNodesSerializer
#     # filter_visualizations = (DjangoFiltervisualization, filters.SearchFilter)
#     filter_fields = ['projectname', 'is_delete']
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         return APIResponse(HTTP_200_OK, 'list success', serializer.data)
#
#
# class SectionEdgesViewSet(GenericViewSet):
#     queryset = SectionEdges.objects.all()
#     serializer_class = SectionEdgesSerializer
#     # filter_visualizations = (DjangoFiltervisualization, filters.SearchFilter)
#     filter_fields = ['projectname', 'is_delete']
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         return APIResponse(HTTP_200_OK, 'list success', serializer.data)


class ClusterDatasFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(Q(cluster=0))


class ClusterDatasViewSet(GenericViewSet):
    queryset = ClusterData.objects.all()
    serializer_class_list = [ClusterDatasReadRootSerializer,
                             ClusterDatasReadTypeSerializer,
                             ClusterReadFileSerializer]
    filter_backends = [ClusterDatasFilter]

    def get_serializer_class_from_list(self, item):
        return self.serializer_class_list[item.cluster](item)

    def serialize_tree(self, queryset):
        for obj in queryset:
            data = self.get_serializer_class_from_list(obj).data
            if obj.cluster != 2:
                data['children'] = self.serialize_tree(obj.children.all())
            yield data

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        print(queryset)
        data = self.serialize_tree(queryset)
        return APIResponse(HTTP_200_OK, 'list success', data)


# def get_cluster_data(request):
#     result_list = post_cluster_data('Launcher3', 14, 'android-10.0.0_r29', 'AGK')
#     result = dict()
#     result['cluster'] = result_list
#     json_str = json.dumps(result, ensure_ascii=False)
#     return JsonResponse(json_str, safe=False)