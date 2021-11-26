from drf_spectacular.utils import OpenApiExample
from core.schema_helper import PAGINATION_DEFAULT, RESPONSE_DEFAULT_LIST, RESPONSE_DEFAULT_PAGINATED, RESPONSE_DEFAULT_RETRIEVE, schema_generator
from social.models import Like


_base_comment = {
    "id": int,
    "is_accepted": bool,
    "reply_to": int,
    'name': str,
    "text": str,
    "hidden": bool,
    "user": int,
    "created_at": "datetime",
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

COMMENT_UPDATE_USER = OpenApiExample(
    name="User",
    value=schema_generator({
        "text": str,
    })
)

COMMENT_UPDATE_ADMIN = OpenApiExample(
    name="Staff user",
    value=schema_generator({
        'name': str,
        "text": str,
        "hidden": bool,
        "is_accepted": bool,
    })
)

COMMENT_RESPONSE_NOREPLY = OpenApiExample(
    **RESPONSE_DEFAULT_LIST,
    value=[schema_generator({
        **_base_comment,
        "replies": None,
    })]
)

LIKE_LIKED_RESPONSE = OpenApiExample(
    name="Liked by user",
    response_only=True,
    value=schema_generator({
        'status': Like.statuses.LIKE,
        'user': int
    }),
    status_codes=['200', '201']
)


LIKE_DISLIKED_RESPONSE = OpenApiExample(
    name="Disliked by user",
    response_only=True,
    value=schema_generator({
        'status': Like.statuses.DISLIKE,
        'user': int
    }),
    status_codes=['200', '201']
)


LIKE_NOTLIKED_RESPONSE = OpenApiExample(
    name="Not liked by user",
    response_only=True,
    value=schema_generator({
        'status': None,
        'user': int
    }),
    status_codes=['200', '201']
)
