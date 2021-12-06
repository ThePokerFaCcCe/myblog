from django_filters.rest_framework.backends import DjangoFilterBackend
from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.viewsets import GenericViewSet

from blog.models import Category, Post, SpecialForChoices
from blog.serializers import CategorySerializer, PostSerializer
from core.permissions import IsAdmin, IsAuthor, IsOwnerOfItem, IsReadOnly
from core.mixins import DeletePicMixin, SandBoxMixin


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


class SpecialMixin:
    def get_special_for_fields(self):
        """Returns a list of fields that contains `SpecialForChoices`"""
        return ['special_for']

    def filterby_special_for(self,
                             queryset,
                             choices: list[SpecialForChoices],
                             status: str = "IS",
                             ):
        """Returns a list of Q filters for every field in `get_special_for_fields`.

        Params
        --------
        `status` can set to "NOT" or "IS".
        """
        not_status = (status == 'NOT')
        for item in self.get_special_for_fields():

            for choice in choices:
                queryset = queryset.filter(
                    ~Q(**{item: choice}) if not_status else Q(**{item: choice})
                )

        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return queryset
            elif user.is_author:
                return self.filterby_special_for(queryset, status="NOT", choices=[SpecialForChoices.STAFF])
            elif user.is_vip:
                return self.filterby_special_for(
                    queryset,
                    status="NOT",
                    choices=[SpecialForChoices.STAFF, SpecialForChoices.AUTHOR]
                )

        return self.filterby_special_for(queryset, choices=[SpecialForChoices.NORMAL])


class CategoryDefaultsMixin(SpecialMixin, SandBoxMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [IsReadOnly | IsAuthor | IsAdmin]


class CategoryDetailMixin(CategoryDefaultsMixin,
                          RetrieveModelMixin, UpdateModelMixin,
                          DeletePicMixin, DestroyModelMixin,
                          GenericViewSet):
    pass


class PostDefaultsMixin(SpecialMixin, SandBoxMixin):
    queryset = Post.objects.select_related("category").prefetch_related("tags__tag", 'likes', 'author', 'comments__user')
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [IsReadOnly | IsAdmin | (IsAuthor & IsOwnerOfItem)]

    def get_special_for_fields(self):
        return ['special_for', 'category__special_for']


class PostDetailMixin(PostDefaultsMixin,
                      RetrieveModelMixin, UpdateModelMixin,
                      DeletePicMixin, DestroyModelMixin,
                      GenericViewSet):
    pass
