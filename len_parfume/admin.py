from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from .models import *


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(),label='Описание')
    class Meta:
        model = Product
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':("name",)}
    list_display= ( 'id','name')
    list_display_links=('id','name')


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':("title",)}
    list_display= ( 'id','title', 'category', 'price', 'available')
    list_display_links=('id','title')
    list_editable=('available',)
    change_form_template = 'custom_admin/change_form.html'
    form = ProductAdminForm
    search_fields=('title',)
    readonly_fields = ('views',)


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':("title",)}
    list_display= ( 'id','title')
    list_display_links=('id','title')

    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name' ,'last_name','final_price', 'created_at' )
    list_display_links=('id','first_name')


class RewiewsAdmin(admin.ModelAdmin):
    list_display = ('id','name','product','data','text')
    list_display_links=('id','name')
    search_fields=('name','text',)


class WhishlistAdmin(admin.ModelAdmin):
    list_display = ('id','owner','products')
    list_display_links=('id','owner')
    search_fields=('owner','products',)

admin.site.register(Category,CategoryAdmin)
admin.site.register(Size)
# admin.site.register(Likes)
admin.site.register(Product,ProductAdmin)
admin.site.register(CartProduct)
admin.site.register(Order,OrderAdmin)
admin.site.register(Customer)
admin.site.register(Whishlist,WhishlistAdmin)
admin.site.register(Rewiews,RewiewsAdmin)




admin.site.site_title="Администрация магазина"
admin.site.site_header="Магазин"