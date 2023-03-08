import json
from rest_framework import serializers
from cluster.models import *


class JsonSerializer(serializers.JSONField):
    default_error_messages = {'invalid_json': '无效的json数据格式'}

    def to_representation(self, value):
        return json.loads(value)

    # 传入json字符串
    def to_internal_value(self, data):
        return data


class ListSerializer(serializers.ListField):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        return ','.join(data)


class CatelogueTreeMapDatasValueListSerializer(serializers.ListField):
    def to_representation(self, value):
        if len(value):
            return list(map(float, value.split(',')))
        return []

    def to_internal_value(self, data):
        return ','.join(map(str, data))


class SubCatelogueDatasSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['version_project'].write_only = True
        self.fields['parent_catelogue'].write_only = True
        self.fields['catelogue_type'].write_only = True

    relation = JsonSerializer()

    class Meta:
        model = CatelogueData
        fields = '__all__'


class CatelogueDatasSerializer(serializers.ModelSerializer):
    children = SubCatelogueDatasSerializer(many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['version_project'].write_only = True

    class Meta:
        model = CatelogueData
        fields = ['id', 'name', 'children', 'catelogue_type', 'version_project']


class CatelogueTreeMapDatasSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['version_project'].write_only = True

    relation = JsonSerializer()
    value = CatelogueTreeMapDatasValueListSerializer()

    class Meta:
        model = TreeMapData
        fields = '__all__'


class CatelogueTreeMapDatasWriteFileSerializer(serializers.ModelSerializer):
    relation = JsonSerializer()
    value = CatelogueTreeMapDatasValueListSerializer()

    class Meta:
        model = TreeMapData
        fields = ['id', 'name', 'color', 'qualifiedName', 'relation', 'value']


class CatelogueTreeMapDatasWritePackageSerializer(serializers.ModelSerializer):
    value = CatelogueTreeMapDatasValueListSerializer()

    class Meta:
        model = TreeMapData
        fields = ['id', 'name', 'color', 'qualifiedName', 'value', 'children']


class CatelogueTreeMapDatasWriteRootSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeMapData
        fields = ['name', 'children']


# class SectionNodesSerializer(serializers.ModelSerializer):
#     mode_type = ListSerializer()
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['version_project'].write_only = True
#
#     class Meta:
#         model = SectionNodes
#         fields = '__all__'
#
#
# class SectionEdgesSerializer(serializers.ModelSerializer):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['version_project'].write_only = True
#
#     class Meta:
#         model = SectionEdges
#         fields = '__all__'


class ClusterDatasSerializer(serializers.ModelSerializer):
    relation = JsonSerializer()

    class Meta:
        model = ClusterData
        fields = '__all__'


class ClusterReadFileSerializer(serializers.ModelSerializer):
    relation = JsonSerializer()

    class Meta:
        model = ClusterData
        fields = ['name', 'id', 'color', 'relation', 'value']


class ClusterDatasReadTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClusterData
        fields = ['name', 'id', 'color', 'children']


class ClusterDatasReadRootSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClusterData
        fields = ['name', 'id', 'children']
