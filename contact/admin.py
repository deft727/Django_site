from django.contrib import admin

from .models import *


@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ["id","name","email"]
    list_display_links = ["name"]

@admin.register(ContactQuestions)
class ContactQuestions(admin.ModelAdmin):
    list_display = ["id","email","message","created_at"]
    list_display_links = ["id","email"]

@admin.register(AboutModel)
class AboutModelAdmin(admin.ModelAdmin):
    list_display = ["id","mini_text"]
    list_display_links = ["id","mini_text"]


@admin.register(FaqModel)
class FaqModelAdmin(admin.ModelAdmin):
    list_display = ["id","question"]
    list_display_links = ["id","question"]

admin.site.register(Social)
admin.site.register(FooterInfo)