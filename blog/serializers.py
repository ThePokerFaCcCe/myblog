from djoser.serializers import (
    UserSerializer as DjoserUserSerializer,
    UserCreatePasswordRetypeSerializer as DjoserUserCreateSerializer
)
from rest_framework import serializers
from blog.models import User

from picturic.serializer_fields import PictureField


class UserCreateSerializer(DjoserUserCreateSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["re_password"] = serializers.CharField(
            style={"input_type": "password"},
            write_only=True,
        )

    class Meta:
        model = User
        fields = list(DjoserUserCreateSerializer.Meta.fields) + [
            'first_name',
            'last_name',
            'birth_date',
        ]


class UserSerializer(DjoserUserSerializer):
    profile_image = PictureField(read_only=True)

    class Meta:
        model = User
        read_only_fields = [
            'email',
            'is_active',
            'is_vip',
            'is_author',
            'is_staff',
            'is_superuser',
            'rank_expire_date',
            'created_at',
            'updated_at',
        ]
        fields = [
            'id',
            'first_name',
            'last_name',
            'birth_date',
            'profile_image',
        ] + read_only_fields
