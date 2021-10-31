from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from social.schemas import COMMENT_RESPONSE_RETRIEVE
from .models import Tag, TaggedItem, Comment


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'label'
        ]


class TaggedItemSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()

    class Meta:
        model = TaggedItem
        fields = [
            'id',
            'label'
        ]

    def get_label(self, obj) -> str:
        return obj.tag.label


@extend_schema_serializer(examples=[COMMENT_RESPONSE_RETRIEVE])
class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    reply_to = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'is_accepted',
            'reply_to',
            'name',
            'email',
            'text',
            'hidden',
            'user',
            'replies',
            'created_at',
        ]
        extra_kwargs = {
            'email': {'write_only': True},
            'is_accepted': {"read_only": True},
            'user': {'read_only': True},
            'hidden': {'read_only': True},
        }

    def validate_reply_to(self, reply):
        if reply:
            if not (
                reply.content_type == self.context.get("content_type")
                and
                reply.object_id == int(self.context.get("object_id"))
            ):
                raise serializers.ValidationError({
                    "reply_to": f"Invalid pk \"{reply}\" - object does not exist."
                })
        return reply

    def get_replies(self, obj):
        return self.__class__(obj.get_children(), many=True, context=self.context).data

    def create(self, validated_data):
        user = self.context['request'].user
        return super().create({**validated_data, "user": user})


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
        ]


class CommentAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
            'is_accepted',
        ]
