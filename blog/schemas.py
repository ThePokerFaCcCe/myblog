from drf_spectacular.utils import OpenApiExample
from rest_framework import serializers
from core.schema_helper import schema_generator

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


class RUDParameters(serializers.Serializer):
    id = serializers.IntegerField(min_value=0, required=False, allow_null=True)
    slug = serializers.SlugField(allow_unicode=True, required=False, allow_null=True)
