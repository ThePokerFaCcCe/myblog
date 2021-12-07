
from django.db.models.base import Model
from django.contrib.contenttypes.models import ContentType
from rest_framework.viewsets import ModelViewSet
from ipware import get_client_ip
from viewcount.models import View


class ViewCountMixin():
    _is_user_first_view = False
    _view_count = None
    _generic_kwargs = None

    def _get_generic_kwargs(self):
        if self._generic_kwargs is None:
            obj = self.get_object()
            self._generic_kwargs = {
                "object_id": obj.pk,
                "content_type": ContentType.objects.get_for_model(obj.__class__),
            }

        return self._generic_kwargs

    def get_view_count(self) -> int:
        """Count model instance views in database"""
        if self._view_count is None:
            self._view_count = View.objects.filter(**self._get_generic_kwargs()).count()

        return self._view_count

    def count_view(self) -> int:
        """Check if user viewed this model instance or not, 
        and increases the view count if user not viewed before.

        this is not very accurate. different users with same IP will
        be counted but one user with different IP will be counted once.
        """
        ip, routable = get_client_ip(self.request)
        user = self.request.user if self.request.user.is_authenticated else None

        # if user:
        #     data = {"user": user,
        #             "defaults": {"ip": ip}
        #             }
        # else:
        #     data = {"ip": ip}
        data = {"user": user,
                "defaults": {"ip": ip}
                }

        view, created = View.objects.get_or_create(
            **(data | self._get_generic_kwargs())
        )
        self._is_user_first_view = created

        return self.get_view_count()

    def get_serializer_context(self):
        return super().get_serializer_context() | {
            "view_count": self.get_view_count(),
            "is_user_first_view": self._is_user_first_view
        }

    def retrieve(self, request, *args, **kwargs):
        self.count_view()
        return super().retrieve(request, *args, **kwargs)
