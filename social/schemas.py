from drf_spectacular.utils import OpenApiExample
from core.schema_helper import PAGINATION_DEFAULT, RESPONSE_DEFAULT_LIST, RESPONSE_DEFAULT_PAGINATED, RESPONSE_DEFAULT_RETRIEVE, schema_generator


_base_comment = {
    "id": int,
    "reply_to": int,
    "text": str,
    "hidden": bool,
    "user": int,
    "created_at": "datetime",
    "updated_at": "datetime",
}

TAG_RESPONSE_RETRIEVE = OpenApiExample(
    **RESPONSE_DEFAULT_RETRIEVE,
    value=schema_generator({
        "id": int,
        "label": str,
    })
)

COMMENT_RESPONSE_RETRIEVE = OpenApiExample(
    **RESPONSE_DEFAULT_RETRIEVE,
    value=schema_generator({
        **_base_comment,
        "replies": [
            {
                **_base_comment,
                'replies': ['...']
            }
        ],
    })
)

COMMENT_RESPONSE_LIST = OpenApiExample(
    **RESPONSE_DEFAULT_LIST,
    value=[COMMENT_RESPONSE_RETRIEVE.value]
)

COMMENT_RESPONSE_PAGINATED = OpenApiExample(
    **RESPONSE_DEFAULT_PAGINATED,
    value={
        **PAGINATION_DEFAULT,
        "results": [{
            **schema_generator({
                **_base_comment,
                "replies": [
                    {
                        **_base_comment,
                        'replies': ['...']
                    }
                ],
            })
        }]
    }
)
