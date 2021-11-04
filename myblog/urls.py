from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/v1/auth/', include("djoser.urls.jwt")),
    path('api/v1/', include("blog.urls")),
    path('api/v1/', include("djoser.urls")),
    path('api/v1/', include("social.urls")),
]\
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
