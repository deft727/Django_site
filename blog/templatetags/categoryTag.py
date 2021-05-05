from django import template
from django.db.models import Count
from blog.models import CategoryBlog

register = template.Library()


@register.simple_tag()
def get_category():
    return CategoryBlog.objects.annotate(cnt=Count('posts')).filter(cnt__gt=0)