
import django_filters
from .models import *

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'email': ['icontains'],
            'name': ["icontains"],
        }

class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            'priority': ['exact'],
            'status': ['exact'],
            'user': ['exact'],
        }

class BucketFilter(django_filters.FilterSet):
    class Meta:
        model = Bucket
        fields = {
            'name': ["icontains"],
        }