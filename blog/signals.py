from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.dispatch import receiver

from .models import Category, Post


def _create_slug_from_title(instance):
    title = instance.title

    slug = slugify(title, allow_unicode=True)
    i = 1

    while instance.__class__.objects.filter(slug=slug).exists():
        slug = slugify(f"{title}-{i}", allow_unicode=True)
        i += 1

    instance.slug = slug


@receiver(pre_save, sender=Category)
def create_slug_from_title_category(sender, *args, **kwargs):
    instance = kwargs['instance']
    if not instance.slug:
        _create_slug_from_title(instance)


@receiver(pre_save, sender=Post)
def create_slug_from_title_post(sender, *args, **kwargs):
    instance = kwargs['instance']
    if not instance.slug:
        _create_slug_from_title(instance)
