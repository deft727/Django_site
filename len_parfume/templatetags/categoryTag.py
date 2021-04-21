from django import template
from blog.models import Category

register = template.Library()


@register.simple_tag()
def get_category():
    return Category.objects.all()