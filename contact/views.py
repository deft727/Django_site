from django.shortcuts import render
from django.views.generic import DetailView,CreateView,View,ListView
from .models import *
from .forms import ContactForms


class ContactView(View):
    def get(self,request):
        contact = ContactModel.objects.last()
        form = ContactForms()
        return render(request,'contacts/contact.html',{"contact":contact, "form":form,'title':'Контакты'})


class CreateContact(CreateView):
    form_class = ContactForms
    success_url = '/'


class AboutView(View):
    def get(self,request):
        about = AboutModel.objects.last()
        form = ContactForms()
        return render(request,'contacts/about.html',{"about":about, "form":form,'title':'О нас'})


class FaqView(ListView):
    models = FaqModel
    template_name='contacts/faq.html'
    context_object_name='faq'
    queryset = FaqModel.objects.all()
    extra_context = {'title':'FAQ'}

