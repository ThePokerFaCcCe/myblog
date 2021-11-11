from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType
from django.http.response import Http404

from .serializers import LikeSerializer
from .models import Like
from .utils import liked_by_user
from core.utils import all_methods


class LikeMixin:
    model_like_field = 'likes'

    def get_serializer_class(self):
        if self.action == 'like':
            return LikeSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'like':
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(detail=True, methods=all_methods('put', 'patch'))
    def like(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        like = liked_by_user(
            getattr(instance, self.model_like_field).all(),
            user=user
        )
        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            like_status = serializer.data.get('status')

            if like:
                like.status = like_status
                like.save()
                status_code = status.HTTP_200_OK
            else:
                like = Like.objects.create(
                    user=user, object_id=instance.pk,
                    status=like_status,
                    content_type=ContentType.objects.get_for_model(instance.__class__),
                )
                status_code = status.HTTP_201_CREATED

            serializer = self.get_serializer(like)
            return Response(serializer.data, status=status_code)

        else:
            if not like:
                return Response(status=status.HTTP_204_NO_CONTENT)

            if request.method == 'GET':
                serializer = self.get_serializer(like)
                return Response(serializer.data)

            elif request.method == 'DELETE':
                like.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
