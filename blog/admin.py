from django.contrib import admin
from django import forms
from .models import Post,CategoryBlog
from ckeditor.widgets import CKEditorWidget


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':("title",)}
    form = PostAdminForm


class CategoryBlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':("title",)}


admin.site.register(Post,PostAdmin)
admin.site.register(CategoryBlog,CategoryBlogAdmin)