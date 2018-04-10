from django import template
from ..models import Banner

register = template.Library()

@register.assignment_tag
def get_last_banner():
    return Banner.objects.last()

@register.filter(name='add_attributes')
def add_attributes(field, css):
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            t, v = d.split(':')
            attrs[t] = v

    return field.as_widget(attrs=attrs)
