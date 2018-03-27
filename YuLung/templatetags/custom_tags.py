from django import template
from ..models import Banner

register = template.Library()

@register.assignment_tag
def get_last_banner():
    return Banner.objects.last()
