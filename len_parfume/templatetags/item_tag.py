from django import template
from len_parfume.models import Product,Whishlist,User
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag(takes_context=True)
def get_item(context,filter):
    request = context ['request']
    if not filter:
        return mark_safe("inactive")
    else:

        # product=Product.objects.get(id=filter)
        if request.user.is_authenticated:
            # user = User.objects.filter(username=request.user).first()
            x=Whishlist.objects.filter(owner=request.user,products__id=filter).exists()
            if x:
                return mark_safe("active")
            else:
                return mark_safe("inactive")
        else:
            name = str(request.session.session_key)
            x=Whishlist.objects.filter(session=name,products__id=filter).exists()
            if x:
                return mark_safe("active")
            else:
                return mark_safe("inactive")



