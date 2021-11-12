from django_filters.rest_framework.backends import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from django.contrib.contenttypes.models import ContentType
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter

from core.paginations import DefaultLimitOffsetPagination
from core.permissions import IsAdmin, IsOwnerOfItem
from core.filters import OrderingFilterWithSchema
from core.utils import all_methods
from social.views import ListCreateCommentsViewset
from social.mixins import LikeMixin
from .models import Post
from .filters import CategoryRUDFilter, PostRUDFilter, PostFilter
from .schemas import (POST_RESPONSE_PAGINATED, POST_RESPONSE_RETRIEVE,
                      USER_EDIT_REQUEST, USER_STAFF_EDIT_REQUEST,
                      USER_SUPER_EDIT_REQUEST, rud_parameters)
from .mixins import (CategoryDefaultsMixin, CategoryDetailMixin,
                     PostDefaultsMixin, PostDetailMixin,
                     RUDWithFilterMixin)
from .serializers import (UserSerializer,
                          UserProfileSerializer,
                          UserStaffEditSerializer, UserSuperEditSerializer)


@extend_schema_view(
    update=extend_schema(
        examples=[USER_EDIT_REQUEST, USER_STAFF_EDIT_REQUEST, USER_SUPER_EDIT_REQUEST]
    ),
    partial_update=extend_schema(
        examples=[USER_EDIT_REQUEST, USER_STAFF_EDIT_REQUEST, USER_SUPER_EDIT_REQUEST]
    ),
    me=extend_schema(
        examples=[USER_EDIT_REQUEST, USER_STAFF_EDIT_REQUEST, USER_SUPER_EDIT_REQUEST]
    ),
)
class UserViewSet(DjoserUserViewSet):

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            if self.request.user.is_superuser:
                return UserSuperEditSerializer
            elif self.request.user.is_staff:
                return UserStaffEditSerializer
            return UserSerializer

        elif self.action in ['profile_image', 'me_profile_image']:
            return UserProfileSerializer

        return super().get_serializer_class()

    @action(detail=True,
            methods=all_methods('post', 'delete', only_these=True),
            permission_classes=[IsOwnerOfItem | IsAdmin],
            parser_classes=[MultiPartParser])
    def profile_image(self, request, *args, **kwargs):
        user = self.get_object()
        if request.method == 'POST':
            serializer = self.get_serializer_class()(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            user.profile_image.delete()
            user.profile_image = None
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=all_methods('post', 'delete', only_these=True),
            permission_classes=[IsOwnerOfItem | IsAdmin],
            parser_classes=[MultiPartParser],
            url_path='me/profile_image'
            )
    def me_profile_image(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.profile_image(request, *args, **kwargs)


class CategoryListViewSet(CategoryDefaultsMixin,
                          ListModelMixin, CreateModelMixin,
                          GenericViewSet):
    pass


@extend_schema(parameters=[rud_parameters])
class CategoryDetailViewSet(RUDWithFilterMixin, CategoryDetailMixin):
    filterset_class = CategoryRUDFilter


@extend_schema(examples=[POST_RESPONSE_PAGINATED])
class PostListViewSet(PostDefaultsMixin,
                      ListModelMixin, CreateModelMixin,
                      GenericViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilterWithSchema]
    filterset_class = PostFilter
    pagination_class = DefaultLimitOffsetPagination
    search_fields = ['title', 'content']
    ordering_fields = ['title', 'updated_at', 'created_at', 'category__title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema_view(  # If i don't use it, it will be shown as response for like view
    retrieve=extend_schema(examples=[POST_RESPONSE_RETRIEVE]),
    update=extend_schema(examples=[POST_RESPONSE_RETRIEVE]),
    partial_update=extend_schema(examples=[POST_RESPONSE_RETRIEVE]),
)
@extend_schema(parameters=[rud_parameters])
class PostDetailViewSet(RUDWithFilterMixin, LikeMixin, PostDetailMixin):
    filterset_class = PostRUDFilter


@extend_schema(parameters=[rud_parameters])
class PostCommentViewSet(ListCreateCommentsViewset):
    content_type = ContentType.objects.get_for_model(Post)
    _oid = None

    def _get_oid(self):
        if not self._oid:
            id = self.request.query_params.get('id')
            slug = self.request.query_params.get('slug')
            where = {"pk": id} if id else {"slug": slug}

            post = get_object_or_404(Post.objects.all(), **where)
            self._oid = post.pk
        return self._oid
