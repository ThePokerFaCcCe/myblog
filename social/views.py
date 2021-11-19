from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from django.http.response import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from social.schemas import COMMENT_RESPONSE_PAGINATED, COMMENT_RESPONSE_RETRIEVE

from core.permissions import IsAdmin, IsAuthor, IsOwnerOfItem, IsReadOnly
from core.utils import all_methods
from core.paginations import DefaultLimitOffsetPagination
from .models import Tag, Comment
from .serializers import CommentAdminUpdateSerializer, CommentUpdateSerializer, TagSerializer, CommentSerializer


@permission_classes([IsReadOnly | IsAuthor | IsAdmin])
class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


@permission_classes([IsReadOnly | IsOwnerOfItem | IsAdmin])
class CommentViewset(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Comment.objects.prefetch_related('reply', 'user').all()
    http_method_names = all_methods('put')

    def get_queryset(self):
        if self.request.method == 'DELETE':
            return Comment.objects.all()
        return self.queryset

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            if self.request.user.is_staff:
                return CommentAdminUpdateSerializer
            return CommentUpdateSerializer
        return CommentSerializer

    def destroy(self, req, *args, **kwargs):
        """if an admin deletes a comment, comment will delete. else, comment will hide"""
        if req.user.is_staff:
            return super().destroy(req, *args, **kwargs)
        else:
            comment = self.get_object()
            if not comment.hidden:
                comment.hidden = True
                comment.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=all_methods('get', only_these=True),
            permission_classes=[permissions.IsAdminUser]
            )
    def hidden_comments(self, req, *args, **kwargs):
        """Last deleted comments by users"""
        hidden_comments = self.get_queryset().filter(hidden=True).order_by('-created_at')
        serializer = self.get_serializer_class()(
            hidden_comments,
            read_only=True,
            context={'no-reply': True},
            many=True
        )

        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(examples=[COMMENT_RESPONSE_PAGINATED]),
    create=extend_schema(examples=[COMMENT_RESPONSE_RETRIEVE])
)
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
class ListCreateCommentsViewset(ListModelMixin, CreateModelMixin, GenericViewSet):
    # You should set `get_content_type`
    # and `object_id_lookup_url`
    # in your subclasses

    queryset = None
    """Custom queryset that contains comments"""

    object_queryset = None
    """The base object queryset for validating object id"""

    _oid = None

    object_id_lookup_url: str = None

    def get_content_type(self) -> ContentType:
        return None

    serializer_class = CommentSerializer
    pagination_class = DefaultLimitOffsetPagination

    def _get_oid(self):
        if not self._oid:
            oid = self.kwargs.get(self.object_id_lookup_url)

            assert isinstance(self.object_queryset, QuerySet), (
                "You should set `object_queryset`"
                "for your `ListCreateCommentsViewset` subclass"
            )
            if not self.object_queryset.filter(pk=oid).exists():
                raise Http404
            self._oid = oid
        return self._oid

    def get_queryset(self):
        queryset = self.queryset
        if not queryset:
            queryset = Comment.objects.filter(
                content_type=self.get_content_type(),
                object_id=self._get_oid(),
            ).prefetch_related("user")

        queryset = queryset.all()

        return queryset.get_cached_trees()

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'object_id': self._get_oid(),
            'content_type': self.get_content_type(),
        }

    def perform_create(self, serializer):
        serializer.save(
            content_type=self.get_content_type(),
            object_id=self._get_oid()
        )
