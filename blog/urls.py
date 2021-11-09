from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import BlogConfig
from .views import (CategoryListViewSet,
                    CategoryDetailViewSet,
                    UserViewSet)

app_name = BlogConfig.name

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('category', CategoryListViewSet, basename='category')

category_detail = CategoryDetailViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path("", include(router.urls)),
    path("category/get/", category_detail, name='category-detail')
]
