from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from core.routers import NestedNoLookupRouter, NoLookupRouter

from .apps import BlogConfig
from .views import (CategoryListViewSet, CategoryDetailViewSet, PostCommentViewSet,
                    PostDetailViewSet, PostListViewSet, UserComplimentViewSet,
                    UserViewSet)

app_name = BlogConfig.name

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

nl_router = NoLookupRouter()
nl_router.register('categories', CategoryListViewSet, basename='category')
nl_router.register('category', CategoryDetailViewSet, basename='category')
nl_router.register('posts', PostListViewSet, basename='post')
nl_router.register('post', PostDetailViewSet, basename='post')

user_nrouter = NestedDefaultRouter(router, 'users', lookup='user')
user_nrouter.register('compliments', UserComplimentViewSet, basename='user-comment')

post_nlrouter = NestedNoLookupRouter(nl_router, 'post')
post_nlrouter.register('comments', PostCommentViewSet, basename='post-comment')


urlpatterns = [
    path("", include(router.urls)),
    path("", include(user_nrouter.urls)),
    path("", include(nl_router.urls)),
    path("", include(post_nlrouter.urls)),
]
