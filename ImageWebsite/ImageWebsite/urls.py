from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from first_app.sitemaps import StaticViewSitemap, BlogSitemap

sitemaps = {
    "pages": StaticViewSitemap,
    "blogs": BlogSitemap,
}

urlpatterns = [
    path("", include("first_app.urls")),
    path("admin/", admin.site.urls),

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]