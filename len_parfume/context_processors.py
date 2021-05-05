from .models import Product,Category,Whishlist
from django.db.models import Count
from django.template import context_processors
import uuid

# from specs.models import ProductFeatures,CategoryFeature
# from django.views.decorators.cache import cache_page
# from django.core.cache import cache

def single_well_info(request):
    categories = Category.objects.annotate(cnt=Count('product')).filter(cnt__gt=0)
    if not request.user.is_authenticated and not request.session.session_key:
        request.session.create()
    if request.user.is_authenticated:
        favorites = Whishlist.objects.filter(owner=request.user)
    else:
        name = str(request.session.session_key)
        favorites = Whishlist.objects.filter(session=name)
    infav=favorites.count()
    return {
        'categories': categories,
        'infav':infav,
    }

