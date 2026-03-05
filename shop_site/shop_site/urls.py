from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/doc/', include("django.contrib.admindocs.urls")),
    path('admin/', admin.site.urls),
    path('api/', include("api.urls")),
    path('users/', include("users.urls")),
]

if settings.DEBUG:
    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
