
from social.models import Like


def count_likes_by_status(likes: list[Like], status) -> int:
    return len(list(filter(
        lambda like: (like.status == status),
        likes
    )))


def liked_by_user(likes: list[Like], user) -> Like:
    like = list(filter(
        lambda like: (like.user == user), likes
    ))
    if like:
        return like[0]
    return []
