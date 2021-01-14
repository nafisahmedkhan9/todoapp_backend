from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import *
from .serializers import *
from .filters import *
from .utils import *
from rest_framework import viewsets, status, filters
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
import json
from django.conf import settings

@csrf_exempt
@transaction.atomic
def signup(request):
    if request.method != 'POST':
        return JsonResponse({'success': False,  'error': f'method {request.method} is not allowed'})

    user_data = json.loads(request.body)

    if User.objects.filter(email=user_data['email']).exists():

        return JsonResponse({"success": False,  "status": "Email already exists. Please login"})
    else:
        try:

            with transaction.atomic():
                user = User.objects.create_user(
                    user_data["email"], user_data["password"])
                user.name = user_data["name"]
                user.email = user_data["email"]
                user.save()
                return JsonResponse({"success": True,  "status": "Successfully registered",
                                     "data": {"user": user.to_dict(), "access_token": user.token}})
        except Exception as e:
            print(str(e))
            return JsonResponse({"success": False, "status": str(e)})

@csrf_exempt
def login(request):

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': f'method {request.method} is not allowed'})

    user_data = json.loads(request.body)

    if User.objects.filter(email=user_data['email']).exists():
        user = User.objects.get(email=user_data['email'])

        if user.check_password(user_data['password']):
            return JsonResponse({"success": True, "status": "Login Successfull",
                                 "data": {"user": user.to_dict(), 'access_token': user.token}})
        else:
            return JsonResponse({"success": False,  "status": "Email/password did not match"})
    else:
        return JsonResponse({"success": False,  "status": "Email does not exist"})


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoints for users
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = UserFilter

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoints for task
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = TaskFilter

    def get_queryset(self):
        return Task.objects.get_user_filtered(self.request.user)

class BucketViewSet(viewsets.ModelViewSet):
    """
    API endpoints for bucket
    """
    queryset = Bucket.objects.all().order_by('id')
    serializer_class = BucketSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = BucketFilter