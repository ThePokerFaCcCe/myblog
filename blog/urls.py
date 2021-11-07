from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import BlogConfig
from .views import (CategoryListViewSet,
                    CategorySlugDetailViewSet, CategoryPKDetailViewSet,
                    UserViewSet)

app_name = BlogConfig.name

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('category', CategoryListViewSet, basename='category')
router.register('category/id', CategoryPKDetailViewSet, basename='category-pk')
router.register('category/slug', CategorySlugDetailViewSet, basename='category-slug')

urlpatterns = [
    path("", include(router.urls))
]
