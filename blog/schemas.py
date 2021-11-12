from drf_spectacular.utils import OpenApiExample, OpenApiParameter
from rest_framework import serializers

from core.schema_helper import (schema_generator,
                                RESPONSE_DEFAULT_RETRIEVE,
                                PAGINATION_DEFAULT, RESPONSE_DEFAULT_PAGINATED)
from social.schemas import TAG_RESPONSE_RETRIEVE
from picturic.schemas import PICTURE_DEFAULT


USER_EDIT_REQUEST = OpenApiExample(
    name='User',
    request_only=True,
    value=schema_generator({
        "first_name": str,
        "last_name": str,
        "birth_date": "date",
    })
)

USER_STAFF_EDIT_REQUEST = OpenApiExample(
    name='Staff User',
    request_only=True,
    value={
        **USER_EDIT_REQUEST.value,
        **schema_generator({
            'email': 'email',
            'is_active': bool,
            'is_vip': bool,
            'is_author': bool,
            'rank_expire_date': "datetime",
        })
    }
)

USER_SUPER_EDIT_REQUEST = OpenApiExample(
    name='Super User',
    request_only=True,
    value={
        **USER_EDIT_REQUEST.value,
        **USER_STAFF_EDIT_REQUEST.value,
        **schema_generator({
            'is_staff': bool,
            'is_superuser': bool,
        })
    }
)


class RUDParametersSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0, required=False, allow_null=True)
    slug = serializers.SlugField(allow_unicode=True, required=False, allow_null=True)


rud_parameters = OpenApiParameter('Get Item', description='Enter either `id` or `slug` for finding item', type=RUDParametersSerializer)

CATEGORY_INFO_DEFAULT = {
    "id": int,
    "title": str,
    "slug": str,
}


POST_RESPONSE_RETRIEVE = OpenApiExample(
    **RESPONSE_DEFAULT_RETRIEVE,
    value=schema_generator({
        "id": int,
        "title": str,
        "slug": str,
        "category": CATEGORY_INFO_DEFAULT,
        "picture": PICTURE_DEFAULT,
        "content": str,
        "author": int,
        "tags": [TAG_RESPONSE_RETRIEVE.value],
        "likes": int,
        "dislikes": int,
        "liked_by_user": bool,
        "created_at": "datetime",
        "updated_at": "datetime"
    })
)

POST_RESPONSE_PAGINATED = OpenApiExample(
    **RESPONSE_DEFAULT_PAGINATED,
    value={
        **PAGINATION_DEFAULT,
        'results': [POST_RESPONSE_RETRIEVE.value]
    }
)
