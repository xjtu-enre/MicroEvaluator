from rest_framework import serializers
from user import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

    extra_kwargs = {
        "id": {
            "read_only": True
        },
        # "password": {
        #     "write_only": True
        # }

    }
