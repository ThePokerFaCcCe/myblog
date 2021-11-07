
class DeletePicMixin:
    def perform_destroy(self, instance):
        instance.picture.delete()
        super().perform_destroy(instance)
