from django.utils.text import slugify
from django.test import TestCase
from uuid import uuid4

from .models import Category, Post, User


def create_author(**kwargs):
    data = {
        "email": f"{uuid4()}@gmail.com",
        "password": 'sss',
        "first_name": 'Matin',
        "last_name": 'Khaleghi',
        'is_author': True,
    }
    return User.objects.create_user(**{**data, **kwargs})


def create_category(**kwargs):
    data = {
        'title': "Lorem"
    }
    return Category.objects.create(**{**data, **kwargs})


def create_post(**kwargs):
    data = {
        'title': "Lorem",
        'content': "Lorem ipsum...",
        'category': create_category(),
        'author': create_author(),
    }
    return Post.objects.create(**{**data, **kwargs})


class CreateSlugTest(TestCase):
    def test_post_slug(self):
        post = create_post(title='Hello joHn')
        slug = slugify(post.title, allow_unicode=True)
        self.assertEqual(post.slug, slug)

    def test_category_slug(self):
        category = create_category(title='big robbers')
        slug = slugify(category.title, allow_unicode=True)
        self.assertEqual(category.slug, slug)
