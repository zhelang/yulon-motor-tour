from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from .models import ServicesType, CustomersType
 
#class ReservationSitemap(Sitemap):
#    changefreq = 'weekly'
#    priority = 0.9
# 
#    def items(self):
#        return ['reservation-index']
#         
#    def location(self, item):
#        return reverse(item)
