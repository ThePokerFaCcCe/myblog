from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import BlogConfig
from .views import (CategoryListViewSet, CategoryDetailViewSet,
                    PostDetailViewSet, PostListViewSet,
                    UserViewSet)

app_name = BlogConfig.name

VIEW_DETAIL = {
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
}

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('category', CategoryListViewSet, basename='category')
router.register('post', PostListViewSet, basename='post')

category_detail = CategoryDetailViewSet.as_view({**VIEW_DETAIL})
post_detail = PostDetailViewSet.as_view({**VIEW_DETAIL})


urlpatterns = [
    path("", include(router.urls)),
    path("category/get/", category_detail, name='category-detail'),
    path("post/get/", post_detail, name='post-detail'),
]
