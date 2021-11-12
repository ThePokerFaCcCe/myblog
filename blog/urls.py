from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.routers import NestedNoLookupRouter, NoLookupRouter

from .apps import BlogConfig
from .views import (CategoryListViewSet, CategoryDetailViewSet, PostCommentViewSet,
                    PostDetailViewSet, PostListViewSet,
                    UserViewSet)

app_name = BlogConfig.name

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

nl_router = NoLookupRouter()
nl_router.register('categories', CategoryListViewSet, basename='category')
nl_router.register('category', CategoryDetailViewSet, basename='category')
nl_router.register('posts', PostListViewSet, basename='post')
nl_router.register('post', PostDetailViewSet, basename='post')

post_nlrouter = NestedNoLookupRouter(nl_router, 'post')
post_nlrouter.register('comments', PostCommentViewSet, basename='post-comment')

urlpatterns = [
    path("", include(router.urls)),
    path("", include(nl_router.urls)),
    path("", include(post_nlrouter.urls)),
]
