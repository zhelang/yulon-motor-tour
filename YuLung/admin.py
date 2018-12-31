from django.contrib import admin
from .models import (
    Banner,
    Comment,
    EmailTemplate,
    FAQ,
    SEO,
    SiteInfo,
    Ticket
)
from .forms import FAQAdminForm, SiteInfoAdminForm


class FAQAdmin(admin.ModelAdmin):
    form = FAQAdminForm


class SiteInfoAdmin(admin.ModelAdmin):
    form = SiteInfoAdminForm


admin.site.register(Banner)
admin.site.register(Comment)
admin.site.register(EmailTemplate)
admin.site.register(SEO)
admin.site.register(Ticket)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(SiteInfo, SiteInfoAdmin)
