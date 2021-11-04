from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from djoser.views import UserViewSet as DjoserUserViewSet

from core.utils import all_methods
from .models import User
from .schemas import USER_EDIT_REQUEST, USER_STAFF_EDIT_REQUEST, USER_SUPER_EDIT_REQUEST
from .serializers import UserSerializer, UserStaffEditSerializer, UserSuperEditSerializer


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
            if self.request.user.is_staff:
                return UserStaffEditSerializer
            return UserSerializer

        return super().get_serializer_class()
