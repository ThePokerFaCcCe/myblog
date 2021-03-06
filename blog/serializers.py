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
from social.serializer_mixins import CommentSerializerMixin, LikeSerializerMixin, TagSerializerMixin
from viewcount.serializer_mixins import ViewCountSerializerMixin
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


class UserSerializer(CommentSerializerMixin,
                     LikeSerializerMixin,
                     DjoserUserSerializer):
    profile_image = PictureField(read_only=True)
    compliments_count = SerializerMethodField()
    posts_count = SerializerMethodField()

    liked_by_user = SerializerMethodField()
    likes = SerializerMethodField()
    dislikes = SerializerMethodField()

    model_comment_field = 'compliments'

    class Meta:
        model = User
        read_only_fields = [
            'email',
            'posts_count',
            'compliments_count',
            "liked_by_user",
            "likes",
            "dislikes",
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

    def get_compliments_count(self, instance) -> int:
        return super().get_comments_count(instance)

    def get_posts_count(self, instance) -> int:
        return instance.posts.count()


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
            'special_for',
            'description',
            'picture',
        ]


class CategoryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'slug',
            'special_for',
        ]


class PostSerializer(DeleteOldPicSerializerMixin,
                     LikeSerializerMixin,
                     TagSerializerMixin,
                     CommentSerializerMixin,
                     UserSerializerMixin,
                     ViewCountSerializerMixin,
                     serializers.ModelSerializer):
    picture = PictureField(required=False, allow_null=True)
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    liked_by_user = SerializerMethodField()
    likes = SerializerMethodField()
    dislikes = SerializerMethodField()
    comments_count = SerializerMethodField()
    view_count = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            "title",
            "slug",
            'special_for',
            "category",
            "picture",
            "content",
            "author",
            'tags',
            'likes',
            'dislikes',
            'liked_by_user',
            'comments_count',
            'view_count',
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            'author': {"read_only": True},
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['category'] = CategoryInfoSerializer(instance.category).data

        return rep


class PostInfoSerializer(LikeSerializerMixin,
                         TagSerializerMixin,
                         CommentSerializerMixin,
                         UserSerializerMixin,
                         ViewCountSerializerMixin,
                         serializers.ModelSerializer):
    picture = PictureField(required=False, allow_null=True)
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    liked_by_user = SerializerMethodField()
    likes = SerializerMethodField()
    dislikes = SerializerMethodField()
    comments_count = SerializerMethodField()
    view_count = SerializerMethodField()

    content = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            "title",
            "slug",
            'special_for',
            "category",
            "picture",
            "content",
            "author",
            'tags',
            'likes',
            'dislikes',
            'liked_by_user',
            'comments_count',
            'view_count',
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

    def get_content(self, instance: Post) -> str:
        content = instance.content
        if len(content) > 50:
            return f"{content[:50]} ..."
        return content
