from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from django.db.models.fields.related import ForeignKey
from django.db.models.fields import TextField
from django.db.models.deletion import PROTECT
from django.db.models.base import Model
from django.core.mail import send_mail
from django.conf import settings
from django.db import models

from social.models import Comment, Like, TaggedItem
from picturic.fields import PictureField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('You should set email')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          password=make_password(password),
                          ** extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=25,
                                  validators=[MinLengthValidator(2, _("first name must have 2 characters or more"))]
                                  )
    last_name = models.CharField(_('last name'), max_length=25,
                                 validators=[MinLengthValidator(2, _("last name must have 2 characters or more"))]
                                 )
    bio = models.TextField(_("Biography"), max_length=160, null=True, blank=True)

    profile_image = PictureField(
        verbose_name=_("Profile image"),
        use_upload_to_func=True, make_thumbnail=True,
        blank=True
    )

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("An account with that email already exists."),
        }
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_("Staff's rank is lower than superuser"),
    )

    is_author = models.BooleanField(
        _('author status'),
        default=False,
        help_text=_("Authors can write post and create category"),
    )

    is_vip = models.BooleanField(
        _("VIP status"),
        default=False
    )

    is_active = models.BooleanField(
        _('active status'),
        default=True,
        help_text=_('Designates whether this user should be treated as active. '),
    )

    rank_expire_date = models.DateTimeField(
        _("Rank expire date"),
        null=True,
        blank=True,
        help_text=_("The date who user's rank will be expired"),
    )

    birth_date = models.DateField(_('birth date'), blank=True, null=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Category(Model):
    title = models.CharField(_("title"), max_length=40)
    slug = models.SlugField(
        allow_unicode=True, editable=False,
        auto_created=True, blank=True, unique=True
    )
    description = models.TextField(_("description"),
                                   max_length=120, null=True, blank=True
                                   )
    picture = PictureField(
        verbose_name=_("Picture"),
        use_upload_to_func=True,
        make_thumbnail=True,
        null=True,
        blank=True
    )


class Post(Model):
    title = models.CharField(_("title"), max_length=80)
    slug = models.SlugField(
        allow_unicode=True, editable=False,
        auto_created=True, blank=True, unique=True
    )
    content = TextField(_("Content"))
    picture = PictureField(
        verbose_name=_("Picture"),
        use_upload_to_func=True,
        make_thumbnail=True,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        _("Updated at"),
        auto_now=True,
    )

    comments = GenericRelation(to=Comment)
    tags = GenericRelation(to=TaggedItem)
    likes = GenericRelation(to=Like)

    category = ForeignKey(
        to=Category, on_delete=PROTECT,
        verbose_name=_("Category"),
    )
    author = ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
        verbose_name=_("Author"),
    )
