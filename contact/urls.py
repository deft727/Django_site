from django.urls import path
from .views import *

urlpatterns = [
    path('contact/',ContactView.as_view(),name='contact'),
    path('about/',AboutView.as_view(),name='about'),
    path('feedback/',CreateContact.as_view(),name='feedback'),
    path('faq/',FaqView.as_view(),name='faq'),
    
]