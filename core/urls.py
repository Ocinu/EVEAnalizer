from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core import settings

urlpatterns = [
    path("select2/", include("django_select2.urls")),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("", include("Bot.urls")),
    path("", include("main.urls")),
    path("", include("pilot.urls")),
    path("universe/", include("universe.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    print(f"!!!! {urlpatterns}")
