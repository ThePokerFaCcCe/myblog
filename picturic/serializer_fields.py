from rest_framework.fields import Field, ImageField
from drf_spectacular.utils import extend_schema_field


@extend_schema_field({'type': "string", 'format': 'binary',
                      'example': {
                          "image": {"url": "string", "name": "string"},
                          "thumbnail": {"url": "string", "name": "string"}
                      }
                      })
class PictureField(ImageField):
    def _make_url(self, value):
        try:
            url = value.url
        except AttributeError:
            return None
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)
        return url

    def _make_data(self, value):
        return {
            'url': self._make_url(value) if value else '',
            'name': value.name if value else '',
        }

    def to_representation(self, value) -> int:
        if not value:
            return None
        # use_url = getattr(self, 'use_url', api_settings.UPLOADED_FILES_USE_URL)
        return {
            'image': self._make_data(value.image),
            'thumbnail': self._make_data(value.thumbnail),
        }

    def to_internal_value(self, data):
        # print('data: ',data.__dict__) # For future usage
        return super().to_internal_value(data)

