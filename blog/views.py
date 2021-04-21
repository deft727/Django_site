from django.shortcuts import render
from django.views.generic import DetailView,View,ListView,CreateView
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404,redirect
from datetime import date,timedelta
from django.utils import timezone
from datetime import datetime, date, time
import datetime


class IndexBlogView(ListView):

    model = Post
    template_name='blog-index.html'
    context_object_name = 'postsblog'
    paginate_by=4
    def get_context_data(self,*,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title']= "Блог"
        return context


class BlogDetailView(DetailView):

    model = Post
    template_name='blog-detail.html'
    context_object_name = 'post'

    def get_context_data(self,*,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title']= "Статья: "+self.get_object().title
        context['form'] =  ReviewsForm()
        return context


class BlogAddReview(View):

    def post(self,request,id):
        if request.user.is_authenticated:
            post = Post.objects.get(id=id)
            lastPost = PostRewiews.objects.last()
            form=ReviewsForm(request.POST or None)
            if  form.is_valid():
                form=form.save(commit=False)
                if lastPost.postId == form.postId:
                    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
                form.name = request.user.username
                form.post=post
                form.save()
            return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
        else:
            return redirect('login')


class BlogCategory(ListView):
    model = Category
    template_name='blog-category.html'
    context_object_name = 'categoryblog'
    slug_url_kwarg = 'slug'

    def get_queryset(self,**kwargs):
        return Post.objects.filter(category__slug=self.kwargs['slug'], is_publish=True)

    def get_context_data(self,*,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='Категория: '+ Post.objects.filter(category__slug=self.kwargs['slug'], is_publish=True).first().title
        return context