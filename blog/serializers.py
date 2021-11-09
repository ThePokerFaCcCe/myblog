from djoser.serializers import (
    UserSerializer as DjoserUserSerializer,
    UserCreatePasswordRetypeSerializer as DjoserUserCreateSerializer
)
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField
from core.serializers import DeleteOldPicSerializerMixin

from picturic.serializer_fields import PictureField
from social.models import Tag
from social.serializer_mixins import LikeSerializerMixin, TagSerializerMixin
from .serializer_mixins import UserSerializerMixin
from .models import Category, User, Post


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


class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = PictureField()

    class Meta:
        model = User
        fields = [
            'id',
            'profile_image'
        ]

    def update(self, instance: User, validated_data):
        instance.profile_image.delete()

        return super().update(instance, validated_data)


class UserStaffEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'birth_date',
            'email',
            'is_active',
            'is_vip',
            'is_author',
            'rank_expire_date',
        ]


class UserSuperEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'birth_date',
            'email',
            'is_active',
            'is_vip',
            'is_author',
            'is_staff',
            'is_superuser',
            'rank_expire_date',
        ]


class UserDeleteSerializer(serializers.Serializer):
    pass


class CategorySerializer(DeleteOldPicSerializerMixin, serializers.ModelSerializer):
    picture = PictureField(required=False, allow_null=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'picture',
        ]


class PostSerializer(DeleteOldPicSerializerMixin,
                     LikeSerializerMixin,
                     TagSerializerMixin,
                     UserSerializerMixin,
                     serializers.ModelSerializer,):
    picture = PictureField(required=False, allow_null=True)
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    liked_by_user = SerializerMethodField()
    likes = SerializerMethodField()
    dislikes = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            "title",
            "slug",
            "category",
            "picture",
            "content",
            "author",
            'tags',
            'likes',
            'dislikes',
            'liked_by_user',
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            'author': {"read_only": True},
        }
