from django.db.models.fields import CharField, DateTimeField, EmailField, PositiveIntegerField, TextField, BooleanField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.fields.related import ForeignKey
from django.db.models.enums import TextChoices
from django.db.models.deletion import CASCADE
from django.db.models.base import Model
from django.utils.html import escape
from django.conf import settings

from mptt.models import MPTTModel, TreeForeignKey

User = settings.AUTH_USER_MODEL


class Tag(Model):
    label = CharField(
        _("Label"),
        max_length=50,
        help_text=_("Tag label")
    )


class TaggedItem(Model):
    tag = ForeignKey(
        to=Tag, on_delete=CASCADE,
        verbose_name=_("Tag"),
        help_text=_("Select tag from created tags")
    )

    content_type = ForeignKey(to=ContentType, on_delete=CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey()


class Like(Model):
    class statuses(TextChoices):
        LIKE = "L", _("Like")
        DISLIKE = "DL", _("Dislike")
    status = CharField(max_length=2, choices=statuses.choices)

    user = ForeignKey(to=User, on_delete=CASCADE, related_name='user_likes')

    content_type = ForeignKey(to=ContentType, on_delete=CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey()


class Comment(MPTTModel):
    text = TextField(_("Text"), max_length=300)
    _name = CharField(_("Name"), max_length=50, null=True, blank=True)
    _email = EmailField(_("Email"), null=True, blank=True)
    hidden = BooleanField(default=False, blank=True)
    created_at = DateTimeField(_("Created at"), auto_now_add=True)
    is_accepted = BooleanField(_("Is accepted"), default=False)
    user = ForeignKey(
        to=User, on_delete=CASCADE,
        null=True, blank=True,
        related_name='comments'
    )

    reply_to = TreeForeignKey(
        to='self', on_delete=CASCADE,
        related_name="reply",
        null=True, blank=True,
        verbose_name=_("Reply to"),
        help_text=_("The message you want to reply")
    )

    content_type = ForeignKey(to=ContentType, on_delete=CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey()

    class MPTTMeta:
        order_insertion_by = ['created_at']
        parent_attr = 'reply_to'

    def clean(self):
        super().clean()
        if self.user:
            self._name = None
            self._email = None
        else:
            self._email = BaseUserManager.normalize_email(self._email)
            self._name = escape(self._name)
        self.text = escape(self.text)

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    @property
    def name(self):
        if self.user:
            return self.user.get_full_name()
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def email(self):
        if self.user:
            return self.user.email
        return self._email

    @email.setter
    def email(self, value: str):
        self._email = value
