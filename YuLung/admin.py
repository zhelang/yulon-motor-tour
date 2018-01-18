from django.contrib import admin
from models import *
from forms import FAQAdminForm , SiteInfoAdminForm

models_list = [Banner, Comment, Ticket, SEO, EmailTemplate]

class FAQAdmin(admin.ModelAdmin):
    form = FAQAdminForm

class SiteInfoAdmin(admin.ModelAdmin):
    form = SiteInfoAdminForm

admin.site.register(models_list)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(SiteInfo, SiteInfoAdmin)
