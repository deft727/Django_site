from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve 
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('',include('len_parfume.urls')),
    path('blog/',include('blog.urls')),
    path('product-specs/', include('specs.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]
# git push -m origin main  
#  git push heroku develop:master 
# git push -f heroku masterbranch:masterbranch 
#    git push -f heroku master:masterbranch      
#  rake assets:precompile   
#git push heroku masterbranch  
# git checkout -b masterbranch
# rm  .git/index.lock 
# rm -f .git/index.lock
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)