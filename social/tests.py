from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from uuid import uuid4

from .models import Comment


def comment_detail_url(pk):
    return reverse("social:comments-detail", args=[pk])


class CommentTest(TestCase):
    def setUp(self):
        self.user = self._create_user()
        self.admin = self._create_user(admin=True)

        self.comment = self._create_comment(self.user)

        self.admin_client = APIClient()
        self.admin_client.force_authenticate(self.admin)

        self.user1_client = APIClient()
        self.user1_client.force_authenticate(self.user)

        self.user2_client = APIClient()
        self.user2_client.force_authenticate(self._create_user())

    def _create_user(self, admin=False):
        data = {
            "email": f"{uuid4()}@gmail.com",
            "password": 'sss',
            "first_name": 'Matin',
            "last_name": 'Khaleghi'
        }

        if admin:
            return get_user_model().objects.create_superuser(
                **data
            )

        return get_user_model().objects.create_user(**data)

    def _create_comment(self, user=None):
        return Comment.objects.create(
            text='Hellow',
            _name='John Doe',
            _email='johndoe@gmail.com',
            user=user,
            content_type=ContentType.objects.get_for_model(self.user),
            object_id=self.user.pk
        )

    def test_create_with_user(self):
        comment = self._create_comment(user=self.user)
        self.assertEqual(comment.email, self.user.email)
        self.assertEqual(comment.name, self.user.get_full_name())

    def test_create_without_user(self):
        comment = self._create_comment()
        self.assertEqual(comment.email, comment._email)
        self.assertEqual(comment.name, comment._name)

    def test_property_setter(self):
        comment = self._create_comment()
        comment.email = 'asd@asd.com'
        comment.name = 'asddd'
        comment.save()
        self.assertEqual(comment.email, comment._email)
        self.assertEqual(comment.name, comment._name)

    def test_bad_property_setter(self):
        comment = self._create_comment()
        comment.email = 'asd3_!&2#><sd.com'
        comment.name = 'b'*69
        comment.save()
        self.assertRaises(ValidationError)

    def test_accept_by_user(self):
        comment = self._create_comment(self.user)
        self.user1_client.patch(
            comment_detail_url(comment.pk),
            {
                "is_accepted": True
            }
        )
        comment.refresh_from_db()
        self.assertEqual(comment.is_accepted, False)

    def test_accept_by_admin(self):
        comment = self._create_comment(self.user)
        self.admin_client.patch(
            comment_detail_url(comment.pk),
            {
                "is_accepted": True
            }
        )
        comment.refresh_from_db()
        self.assertEqual(comment.is_accepted, True)

    def test_edit_by_owner(self):
        comment = self._create_comment(self.user)
        new_text = 'Hiiii'
        res = self.user1_client.patch(
            comment_detail_url(comment.pk),
            {
                "text": new_text
            }
        )
        comment.refresh_from_db()
        self.assertEqual(
            res.status_code, status.HTTP_200_OK,
            msg=res.status_code
        )
        self.assertEqual(
            comment.text, new_text,
            msg=comment.text
        )

    def test_edit_by_another_user(self):
        comment = self._create_comment(self.user)
        res = self.user2_client.patch(
            comment_detail_url(comment.pk),
            {
                "text": 'Hiiii'
            }
        )
        self.assertEqual(
            res.status_code, status.HTTP_403_FORBIDDEN,
            msg=res.status_code
        )
