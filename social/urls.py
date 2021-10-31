from django.urls import path, include
from rest_framework import routers

from .views import TagViewset, CommentViewset
from .apps import SocialConfig

app_name = SocialConfig.name

router = routers.DefaultRouter()
router.register('tags', TagViewset, basename='tags')
router.register('comments', CommentViewset, basename='comments')

urlpatterns = [
    path('', include(router.urls))
]
