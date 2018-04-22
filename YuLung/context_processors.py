from django.conf import settings
import itertools

def static_vars(request):
    return {
        'site_mail': 'tour@yulon-motor.com.tw',
        'base_url': settings.BASE_URL
    }
