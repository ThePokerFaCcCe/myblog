from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.viewsets import GenericViewSet

from blog.models import Category, Post
from blog.serializers import CategorySerializer, PostSerializer
from core.permissions import IsAdmin, IsAuthor, IsOwnerOfItem, IsReadOnly
from core.mixins import DeletePicMixin


class RUDWithFilterMixin:
    filter_backends = [DjangoFilterBackend]
    filterset_class = None
    """You should set `filterset_class` in subclasses"""

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset)
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class CategoryDefaultsMixin:
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [IsReadOnly | IsAuthor | IsAdmin]


class CategoryDetailMixin(CategoryDefaultsMixin,
                          RetrieveModelMixin, UpdateModelMixin,
                          DeletePicMixin, DestroyModelMixin,
                          GenericViewSet):
    pass


class PostDefaultsMixin:
    queryset = Post.objects.select_related("category")
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [IsReadOnly | IsAdmin | (IsAuthor & IsOwnerOfItem)]


class PostDetailMixin(PostDefaultsMixin,
                      RetrieveModelMixin, UpdateModelMixin,
                      DeletePicMixin, DestroyModelMixin,
                      GenericViewSet):
    pass
