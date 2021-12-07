from rest_framework import status
from rest_framework.test import APIClient
from django.utils.http import urlencode
from django.utils.text import slugify
from django.urls.base import reverse
from django.test import TestCase
from uuid import uuid4
from PIL import Image
import tempfile
import os

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


def create_post(only_data=False, **kwargs):
    data = {
        'title': "Lorem",
        'content': "Lorem ipsum...",
        'category': create_category(),
        'author': create_user(is_author=True),
    }
    data = {**data, **kwargs}

    if only_data:
        data.pop('author', None)
        data['category'] = data['category'].pk
        return data
    return Post.objects.create(**data)


def create_comment_data(user, reply_to: int = ''):
    return {
        "user": user.id,
        "text": 'Hellow',
        "reply_to": reply_to,
    }


class CreateSlugTest(TestCase):
    def test_post_slug(self):
        post = create_post(title='Hello joHn')
        slug = slugify(post.title, allow_unicode=True)
        self.assertEqual(post.slug, slug)

    def test_category_slug(self):
        category = create_category(title='big robbers')
        slug = slugify(category.title, allow_unicode=True)
        self.assertEqual(category.slug, slug)

    def test_duplicate_slug(self):
        category1 = create_category(title='big robbers')
        category2 = create_category(title='big robbers')
        self.assertNotEqual(category1.slug, category2.slug)

    def test_edit_slug(self):
        category = create_category(title='big robbers')
        old_slug = category.slug

        category.title = 'hello world'
        category.save()

        self.assertEqual(category.slug, old_slug)


class UserTest(TestCase):
    def _user_url(self, pk):
        return reverse("blog:users-detail", args=[pk])

    def _user_profile_url(self, pk):
        return reverse("blog:users-profile-image", args=[pk])

    def _user_compliments_url(self, pk):
        return reverse("blog:user-comment-list", args=[pk])

    def _send_compliment(self, client, complimenter, user):
        res = client.post(
            self._user_compliments_url(user.pk),
            create_comment_data(complimenter)
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, msg="Send compliment error")

    def _post_detail_url(self, pk):
        return f"{reverse('blog:post-detail')}?{urlencode({'id':pk})}"

    def _post_create_url(self):
        return reverse('blog:post-list')

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

    def test_input_safety(self):
        bad_input = "<script>burn()</script>"
        u = create_user(first_name=bad_input, last_name=bad_input, bio=bad_input)
        self.assertNotEqual(u.first_name, bad_input)
        self.assertNotEqual(u.last_name, bad_input)
        self.assertNotEqual(u.bio, bad_input)

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

    def test_upload_profile_image(self):
        with tempfile.NamedTemporaryFile(suffix='.jpg') as f:
            img = Image.new('RGB', (10, 10))
            img.save(f, format='JPEG')
            f.seek(0)  # Set pointer at first of file
            res = self.user_client.post(
                self._user_profile_url(self.user.pk),
                data={'profile_image': f},
                format='multipart')

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK, msg=res.data)
        self.assertIn('profile_image', res.data)
        self.assertTrue(os.path.exists(self.user.profile_image.image.path))
        self.user.profile_image.delete()

    def test_delete_profile_by_other(self):
        user2 = create_user()
        res = self.user_client.delete(
            self._user_profile_url(user2.pk),
            data=self.data,
        )

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_compliments_count(self):
        count = 3
        for _ in range(count):
            self._send_compliment(self.user_client, self.user, self.staffuser)

        res = self.staffuser_client.get(
            self._user_url(self.staffuser.pk)
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['compliments_count'], count)

        res = self.staffuser_client.get(
            self._user_url(self.user.pk)
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['compliments_count'], 0)

    def test_posts_count(self):
        res = self.staffuser_client.post(
            self._post_create_url(),
            data=create_post(only_data=True)
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.staffuser_client.get(
            self._user_url(self.staffuser.pk)
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['posts_count'], 1)


class PostTest(TestCase):
    def _post_detail_url(self, pk):
        return f"{reverse('blog:post-detail')}?{urlencode({'id':pk})}"

    def _post_detail_like_url(self, pk):
        return f"{reverse('blog:post-like')}?{urlencode({'id':pk})}"

    def _post_create_url(self):
        return reverse('blog:post-list')

    def setUp(self) -> None:
        self.staffuser = create_user(is_staff=True)
        self.author = create_user(is_author=True)
        self.user = create_user()

        self.staffuser_client = APIClient()
        self.staffuser_client.force_authenticate(self.staffuser)

        self.author_client = APIClient()
        self.author_client.force_authenticate(self.author)

        self.user_client = APIClient()
        self.user_client.force_authenticate(self.user)

    def test_create_by_author(self):
        res = self.author_client.post(
            self._post_create_url(),
            create_post(only_data=True),
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_by_user(self):
        res = self.user_client.post(
            self._post_create_url(),
            create_post(only_data=True),
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_by_another_author(self):
        post = create_post(author=self.author)
        author2_client = APIClient()
        author2_client.force_authenticate(create_user(is_author=True))
        res = author2_client.patch(
            self._post_detail_url(post.pk),
            {
                'title': "New title2"
            }
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_by_staff(self):
        post = create_post(author=self.author)
        res = self.staffuser_client.patch(
            self._post_detail_url(post.pk),
            {
                'title': "New title2"
            }
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_likes(self):
        post = create_post()
        like_url = self._post_detail_like_url(post.pk)

        # Test no content result if there isn't liked by user
        res = self.user_client.get(like_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], None)

        # Test liked successfully
        res = self.user_client.post(
            like_url,
            {
                'status': "L"
            }
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, msg=res.data)

        # Test liked_by_user is True for user
        res = self.user_client.get(self._post_detail_url(post.pk))
        self.assertEqual(res.data['likes'], 1)
        self.assertEqual(res.data['dislikes'], 0)
        self.assertEqual(res.data['liked_by_user'], True)

        # Test liked_by_user isn't True for all
        res = self.staffuser_client.get(self._post_detail_url(post.pk))
        self.assertEqual(res.data['liked_by_user'], None)

        # Test disliked successfully
        res = self.user_client.post(
            like_url,
            {
                'status': "DL"
            }
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)  # 200 bcs it's updated, not created!

        # Test liked_by_user is False for user
        res = self.user_client.get(self._post_detail_url(post.pk))
        self.assertEqual(res.data['likes'], 0)
        self.assertEqual(res.data['dislikes'], 1)
        self.assertEqual(res.data['liked_by_user'], False)

    def _get_post(self, client, post, REMOTE_ADDR="127.0.0.1"):
        res = client.get(
            self._post_detail_url(post.pk),
            REMOTE_ADDR=REMOTE_ADDR
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        return res

    def test_view_count(self):
        post = create_post()

        guest_client = APIClient()
        self._get_post(guest_client, post, '192.1.1.4')  # 1
        self._get_post(guest_client, post, '192.1.1.4')  # 1
        self._get_post(guest_client, post)  # 1

        self._get_post(self.user_client, post)  # 2
        self._get_post(self.user_client, post, '155.3.4.51')  # 2

        res = self._get_post(self.staffuser_client, post)  # 3
        self.assertEqual(res.data['view_count'], 3)


class SpecialForTest(TestCase):

    def setUp(self) -> None:
        self.staffuser = create_user(is_staff=True)
        self.author = create_user(is_author=True)
        self.vip = create_user(is_vip=True)
        self.user = create_user()

        self.staffuser_client = APIClient()
        self.staffuser_client.force_authenticate(self.staffuser)

        self.author_client = APIClient()
        self.author_client.force_authenticate(self.author)

        self.vip_client = APIClient()
        self.vip_client.force_authenticate(self.vip)

        self.user_client = APIClient()
        self.user_client.force_authenticate(self.user)

        create_post(special_for='S')
        create_post(special_for='A')
        create_post(special_for='V')
        create_post()

        self.post_list_url = reverse('blog:post-list')

    def _post_detail_url(self, pk):
        return f"{reverse('blog:post-detail')}?{urlencode({'id':pk})}"

    def test_user_get(self):
        res = self.user_client.get(self.post_list_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)

    def test_vip_get(self):
        res = self.vip_client.get(self.post_list_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)

    def test_author_get(self):
        res = self.author_client.get(self.post_list_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 3)

    def test_staff_get(self):
        res = self.staffuser_client.get(self.post_list_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 4)

    def test_special_category_post_is_hidden(self):
        category = create_category(special_for='V')
        post = create_post(category_id=category.pk)  # special_for is 'N'

        res = self.user_client.get(
            self._post_detail_url(post.pk)
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
