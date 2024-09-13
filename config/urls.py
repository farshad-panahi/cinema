from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

from apps.cinema.api import MovieViewSet

from pages.views import HomePage
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("movies", MovieViewSet, basename="movies")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomePage.as_view(), name="home-page"),
    path("api/", include(router.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
