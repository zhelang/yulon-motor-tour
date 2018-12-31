from django.contrib.sitemaps import Sitemap
from .models import ServicesType


class ServiceSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return ServicesType.objects.filter(active=True)
