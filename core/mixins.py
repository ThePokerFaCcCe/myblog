
from django.db.models.query import QuerySet
from rest_framework.viewsets import ModelViewSet


class DeletePicMixin:
    def perform_destroy(self, instance):
        instance.picture.delete()
        super().perform_destroy(instance)


class SandBoxMixin:
    def _add_dbname_to_queryset(self, queryset: QuerySet):
        """Checks "sandbox" is in subdomain or not. 
        if true, adds `.using("sandbox")` to `queryset`"""

        is_sandbox = (getattr(self.request, 'subdomain', None) == 'sandbox')
        if is_sandbox:
            queryset = queryset.using("sandbox")
        return queryset

    get_custom_queryset = _add_dbname_to_queryset

    def get_queryset(self):
        """
        IMPORTANT:
        ---------
        Make sure to call `super().get_queryset()` in your subclass
        """
        return self._add_dbname_to_queryset(
            queryset=super().get_queryset()
        )
