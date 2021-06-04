from django import template
from contact.models import Social,FooterInfo

register = template.Library()


@register.simple_tag()
def get_social_links():
    return Social.objects.all()

@register.simple_tag()
def get_contact():
    return FooterInfo.objects.last()
