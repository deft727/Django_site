from django import template
from len_patfumes.models import Social,FooterInfo

register = template.Library()


@register.simple_tag()
def get_social_links():
    return Social.objects.all()
