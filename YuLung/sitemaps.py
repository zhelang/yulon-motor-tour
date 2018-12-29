from django.contrib.sitemaps import Sitemap
from django.urls import reverse
 
class StaticSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5
 
    def items(self):
        return ['index', 'tos', 'privacy', 'comments', 'faq']
         
    def location(self, item):
        return reverse(item)
