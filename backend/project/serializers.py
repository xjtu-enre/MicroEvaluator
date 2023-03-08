import json
from rest_framework import serializers

from project import models


class VersionProjectSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Version
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    ver = serializers.CharField(write_only=True)

    def validate_projectname(self, name):
        exists = models.Project.objects.filter(projectname=name).exists()
        if exists:
            raise serializers.ValidationError("项目名不能重复")
        return name

    def create(self, validated_data):
        versions = validated_data.pop('ver').split(';')
        pro = models.Project.objects.create(**validated_data)
        for ver in versions:
            models.Version.objects.create(project=pro, version=ver)
        return pro

    class Meta:
        model = models.Project
        fields = '__all__'