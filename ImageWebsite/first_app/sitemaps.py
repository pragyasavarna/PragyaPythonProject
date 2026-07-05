from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.urls.resolvers import RoutePattern

from . import urls
from .models import BlogPost


class StaticViewSitemap(Sitemap):
    protocol = "https"

    def items(self):
        ignored_names = {
            # Authentication
            "login",
            "logout",
            "register",
            "forgot_password",
            "reset_password",

            # Admin
            "admin:index",

            # Backend/AJAX endpoints
            "process_text",
            "summarize_text",
            "save_execution",
            
            # Special files
            "robots",
        }

        pages = []

        for pattern in urls.urlpatterns:

            # Skip unnamed URLs
            if getattr(pattern, "name", None) is None:
                continue

            # Skip ignored URLs
            if pattern.name in ignored_names:
                continue

            # Skip URLs requiring parameters
            if isinstance(pattern.pattern, RoutePattern):
                if "<" in pattern.pattern._route:
                    continue

            pages.append(pattern.name)

        # Remove duplicates while preserving order
        return list(dict.fromkeys(pages))

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    protocol = "https"

    def items(self):
        return (
            BlogPost.objects
            .filter(slug__isnull=False)
            .exclude(slug="")
            .order_by("-published_at")
        )

    def location(self, obj):
        return reverse(
            "blog_detail",
            kwargs={"slug": obj.slug},
        )

    def lastmod(self, obj):
        return obj.published_at