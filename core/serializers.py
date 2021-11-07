from .utils import delete_pic_if_new_exists


class DeleteOldPicSerializerMixin:
    def update(self, instance, validated_data):
        delete_pic_if_new_exists(instance, validated_data)
        return super().update(instance, validated_data)
