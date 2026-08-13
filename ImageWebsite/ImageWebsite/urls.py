from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.conf import settings
from first_app.sitemaps import StaticViewSitemap, BlogSitemap
from django_otp.admin import OTPAdminSite

sitemaps = {
    "pages": StaticViewSitemap,
    "blogs": BlogSitemap,
}

admin.site.__class__ = OTPAdminSite

urlpatterns = [
    path("", include("first_app.urls")),
    path(settings.ADMIN_URL, admin.site.urls),

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]