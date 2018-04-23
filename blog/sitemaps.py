from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    #returns queryset objects to return in the sitemap
    def items(self):
        return Post.published.all()

    #returns last time the object was modified
    def lastmod(self, obj):
        return obj.publish
