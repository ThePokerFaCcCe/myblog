from drf_spectacular.utils import extend_schema, extend_schema_view
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from core.permissions import IsAdmin, IsOwnerOfItem
from core.utils import all_methods
from .mixins import CategoryDefaultsMixin, CategoryDetailMixin
from .schemas import USER_EDIT_REQUEST, USER_STAFF_EDIT_REQUEST, USER_SUPER_EDIT_REQUEST
from .serializers import (UserSerializer,
                          UserProfileSerializer, UserStaffEditSerializer,
                          UserSuperEditSerializer)


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


class CategoryPKDetailViewSet(CategoryDetailMixin):
    lookup_field = 'id'


class CategorySlugDetailViewSet(CategoryDetailMixin):
    lookup_field = 'slug'
