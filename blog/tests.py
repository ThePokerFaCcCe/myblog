from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.utils.text import slugify
from django.test import TestCase
from uuid import uuid4

from .models import Category, Post, User


def create_user(**kwargs):
    data = {
        "email": f"{uuid4()}@gmail.com",
        "password": 'sss',
        "first_name": 'Matin',
        "last_name": 'Khaleghi',
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
        'author': create_user(is_author=True),
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


class UserTest(TestCase):
    def _user_url(self, pk):
        return reverse("blog:users-detail", args=[pk])

    def setUp(self) -> None:
        self.superuser = create_user(is_superuser=True, is_staff=True)
        self.staffuser = create_user(is_staff=True)
        self.user = create_user()

        self.superuser_client = APIClient()
        self.superuser_client.force_authenticate(self.superuser)

        self.staffuser_client = APIClient()
        self.staffuser_client.force_authenticate(self.staffuser)

        self.user_client = APIClient()
        self.user_client.force_authenticate(self.user)

        self.data = {
            'first_name': "John",
            'is_vip': True,
            'is_staff': True,
            'is_superuser': True,
        }

    def test_edit_self_user(self):
        res = self.user_client.patch(
            self._user_url(self.user.pk),
            data=self.data,
        )
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, self.data['first_name'])
        self.assertEqual(self.user.is_vip, False)
        self.assertEqual(self.user.is_staff, False)
        self.assertEqual(self.user.is_superuser, False)

    def test_edit_other_user_by_user(self):
        user2 = create_user()
        res = self.user_client.patch(
            self._user_url(user2.pk),
            data=self.data,
        )

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_edit_user_by_staff(self):
        user2 = create_user()
        res = self.staffuser_client.patch(
            self._user_url(user2.pk),
            data=self.data,
        )
        user2.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(user2.first_name, self.data['first_name'])
        self.assertEqual(user2.is_vip, True)
        self.assertEqual(user2.is_staff, False)
        self.assertEqual(user2.is_superuser, False)

    def test_edit_user_by_super(self):
        user2 = create_user()
        res = self.superuser_client.patch(
            self._user_url(user2.pk),
            data=self.data,
        )
        user2.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(user2.first_name, self.data['first_name'])
        self.assertEqual(user2.is_vip, True)
        self.assertEqual(user2.is_staff, True)
        self.assertEqual(user2.is_superuser, True)
