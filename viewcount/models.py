from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import GenericIPAddressField, PositiveIntegerField
from django.db.models.fields.related import ForeignKey

User = settings.AUTH_USER_MODEL


class View(Model):
    user = ForeignKey(to=User, on_delete=SET_NULL, null=True)
    ip = GenericIPAddressField(unpack_ipv4=True)

    content_type = ForeignKey(to=ContentType, on_delete=CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey()
