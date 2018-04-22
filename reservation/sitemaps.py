from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from .models import ServicesType
 
class ServiceSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
 
    def items(self):
        return ServicesType.objects.filter(active=True)
