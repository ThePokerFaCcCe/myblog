from django.contrib.contenttypes.models import ContentType

from .models import Like, TaggedItem
from .utils import count_likes_by_status, liked_by_user
from .serializers import TaggedItemSerializer


class LikeSerializerMixin:
    model_like_field = 'likes'
    """You can change this in your subclass"""

    def _get_likes(self, instance):
        return getattr(instance, self.model_like_field).all()

    def get_liked_by_user(self, instance) -> bool:
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            like = liked_by_user(
                self._get_likes(instance),
                user=request.user)

            if like:
                return like.status == Like.statuses.LIKE

        return None

    def get_likes(self, instance) -> int:
        return count_likes_by_status(
            self._get_likes(instance),
            status=Like.statuses.LIKE
        )

    def get_dislikes(self, instance) -> int:
        return count_likes_by_status(
            self._get_likes(instance),
            status=Like.statuses.DISLIKE
        )


class TagSerializerMixin:
    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        instance = super().create(validated_data)

        if tags:
            ctype = ContentType.objects.get_for_model(instance.__class__)

            TaggedItem.objects.bulk_create([
                TaggedItem(tag=tag, content_type=ctype, object_id=instance.pk)
                for tag in tags
            ])

        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['tags'] = TaggedItemSerializer(instance.tags, many=True).data
        return rep


class CommentSerializerMixin:
    model_comment_field = 'comments'
    """You can change this in your subclass"""

    def get_comments_count(self, instance) -> int:
        return instance.comments.all().count()
