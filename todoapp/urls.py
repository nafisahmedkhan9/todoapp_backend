from django.conf.urls import url, include
from . import views
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('user', views.UserViewSet)
router.register('task', views.TaskViewSet)
router.register('bucket', views.BucketViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/signup/',  views.signup, name='signup'),
    path('api/login/', views.login, name='login'),
]