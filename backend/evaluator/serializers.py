from rest_framework import serializers
from evaluator.models import *


# class ModuleDataListSerializer(serializers.ListSerializer):
#     def create(self, validated_data):
#         module_data = [ModuleData(**item) for item in validated_data]
#         return ModuleData.objects.bulk_create(module_data)


# class ClassDataListSerializer(serializers.ListSerializer):
#     def create(self, validated_data):
#         # class_data = list()
#         # for item in validated_data:
#         #     module_ids = item.pop('module_ids')
#         #     module = [int(i) for i in module_ids.split(';')]
#         #     classdata = ClassData.objects.create(**item)
#         #     classdata.module.set(module)
#         #     class_data.append(classdata)
#         class_data = [ClassData(**item) for item in validated_data]
#         return ClassData.objects.bulk_create(class_data)


# class ProjectDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProjectData
#         fields = '__all__'
#
#
# class ModuleDataSerializer(serializers.ModelSerializer):
#     # project_name = serializers.CharField(write_only=True)
#
#     class Meta:
#         # list_serializer_class = ModuleDataListSerializer
#         model = ModuleData
#         fields = '__all__'
#
#
# class ClassDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ClassData
#         fields = '__all__'
#         # list_serializer_class = ClassDataListSerializer
#
#
# class MethodDataSerializer(serializers.ModelSerializer):
#     # classname = ClassDataSerializer(many=True)
#
#     class Meta:
#         model = MethodData
#         fields = '__all__'

    # def create(self, validated_data):
    #     classes_name = validated_data.pop('classname')
    #     methoddata = MethodData.objects.create(**validated_data)
    #
    #     for name in classes_name:
    #         class_instance, created = ClassData.objects.get_or_create(index=name["index"])
    #         methoddata.tags.add(class_instance)
    #     return methoddata
