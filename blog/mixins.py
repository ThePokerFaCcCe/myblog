from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet

from blog.models import Category
from blog.serializers import CategorySerializer
from core.permissions import IsAdmin, IsAuthor, IsReadOnly
from core.mixins import DeletePicMixin


class CategoryDefaultsMixin:
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsReadOnly | IsAuthor | IsAdmin]


class CategoryDetailMixin(CategoryDefaultsMixin,
                          RetrieveModelMixin, UpdateModelMixin,
                          DeletePicMixin, DestroyModelMixin,
                          GenericViewSet):
    pass
