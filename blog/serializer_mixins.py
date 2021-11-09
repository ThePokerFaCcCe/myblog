from rest_framework import serializers

from picturic.serializer_fields import PictureField
from .models import User


class UserInfoSerializer(serializers.ModelSerializer):
    # I have to write serializer here, because of circular import.
    profile_image = PictureField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'birth_date',
            'profile_image',
            'is_active',
            'is_vip',
            'is_author',
            'is_staff',
        ]
        read_only_fields = fields


class UserSerializerMixin:
    model_user_field = 'author'
    """You can change this in your subclass"""

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        user = getattr(instance, self.model_user_field)
        rep['author'] = UserInfoSerializer(user).data
        return rep
