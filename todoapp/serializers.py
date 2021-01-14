from rest_framework import serializers
from .models import *


def represent(instance, serializer):
    return None if instance is None else serializer(instance).data

def represent_list(instances, serializer):
    result = []
    for instance in instances.all():
        result.append(represent(instance, serializer))
    return result


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email")


class BucketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bucket
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(serializers.ModelSerializer, self).to_representation(instance)
        representation['bucket'] = represent(instance.bucket, BucketSerializer)
        representation['user'] = represent(instance.user, UserSerializer)
        return representation
