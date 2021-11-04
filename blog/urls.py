from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet
from .apps import BlogConfig

app_name = BlogConfig.name

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path("", include(router.urls))
]
