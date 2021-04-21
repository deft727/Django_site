from django.urls import path
from .views import *

urlpatterns = [

    path('',IndexBlogView.as_view(),name='blog'),
    path('post/<str:slug>/',BlogDetailView.as_view(),name='post'),
    path('addcomment/<int:id>/',BlogAddReview.as_view(),name='addcomment'),
    path('category/<str:slug>/',BlogCategory.as_view(),name='category'),
    ]