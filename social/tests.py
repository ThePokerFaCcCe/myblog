from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Comment


class CommentTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="matin.khaleghi.nezhad@gmail.com",
            password='sss',
            first_name='Matin',
            last_name='Khaleghi'
        )

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
