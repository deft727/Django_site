from django.shortcuts import render,HttpResponsePermanentRedirect,redirect,reverse,HttpResponseRedirect,get_object_or_404
from django.db import transaction
from django.views.generic import DetailView,View,ListView
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.db.models import Q
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.template.loader import render_to_string,get_template
from django.http import Http404
from .utils import CusomerMixin,FinalPrice
from .models import *
from blog.models import Post
from .forms import RegistrationForm,LoginForm,ReviewsForm,OrderForm
from specs.models import ProductFeatures
from cart.cart import Cart


def custom_404(request):
    return render(request, '404/404.html', {}, status=404)


def cart_add(request, id):
    cart = Cart(request)
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
    cart.add(product=product)
    messages.add_message(request,messages.SUCCESS,'Товар добавлен в избранноe')
    try:
        return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
    except:
        return redirect('home')



def item_clear(request, id):
    cart = Cart(request)
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        try:
            return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
        except:
            return redirect('home')
    cart.remove(product)
    try:
        return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
    except:
        return redirect('home')


def item_increment(request, id):
    cart = Cart(request)
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        try:
            return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
        except:
            return redirect('home')
    cart.add(product=product)
    try:
        return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
    except:
        return redirect('home')
    

def item_decrement(request, id):
    cart = Cart(request)
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        try:
            return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
        except:
            return redirect('home')
    cart.decrement(product=product)
    try:
        return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
    except:
        return redirect('home')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    try:
        return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
    except:
        return redirect('home')


def cart_detail(request):
    try:
        return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
    except:
        return redirect('home')



class IndexView(CusomerMixin,View):
    def get(self,request,*args,**kwargs):
        products = Product.objects.filter(available=True)
        new_item = products.filter(in_top=True).order_by('-pk')[:4]
        parfumes = products.filter(category__name='Парфюмерия')[:6]
        probes = products.filter(category__name='Пробники')[:6]
        accessories = products.filter(category__name='Аксессуары')[:6]
        title = 'Elena-Shop :: Parfume storage'
        blog = Post.objects.filter(is_publish=True).order_by('-pk')[:2]
        context= {
            'title': title ,
            'parfumes' : parfumes,
            'probes':probes,
            'accessories':accessories,
            'new_items':new_item,
            'posts':blog
        }
        return render(request,'index.html',context)


class RegistrationView(View):
    def get(self,request,*args,**kwargs):
        if  request.user.is_authenticated:
            # messages.add_message(request,messages.ERROR,'Вы уже зарегистрированы')
            return redirect('home')
        form=RegistrationForm(request.POST or None)
        title = 'Регистрация'
        context = {
            'title':title,
            'form':form,
        }
        return render(request,'registration.html',context)
    
    def post(self,request,*args,**kwargs):
        form= RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.username=form.cleaned_data['username']
            new_user.email=form.cleaned_data['email']
            # new_user.first_name=form.cleaned_data['first_name']
            # new_user.last_name=form.cleaned_data['last_name']
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            # были ли заказы как анонима
            oldname = request.session.session_key
            oldorders = Order.objects.filter(customer__user__username=oldname)
            customer = Customer.objects.create(
                user=new_user,
                # phone=form.cleaned_data['phone'],
            )
            customer.save()
            # если были переносим и удаляем старый заказ
            if oldorders:
                customer.orders.set(oldorders)
                for i in oldorders:
                    i.customer = customer
                    i.customer.save()
                    i.save()
                
                User.objects.filter(username=oldname).delete()
                
            user= authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            login(request,user)
            # messages.add_message(request,messages.SUCCESS,'Вы успешно зарегистрировались на сайте')
            return redirect('home')
        # else:
        #     messages.add_message(request,messages.ERROR,'Ошибка регистрации')
        context={'form':form,}
        return render(request,'registration.html',context)


class LoginView(View):
    def get(self,request,*args,**kwargs):
        if  request.user.is_authenticated:
            # messages.add_message(request,messages.ERROR,'Вы уже залогинены')
            return redirect('home')
        form = LoginForm(request.POST or None)
        # category = Category.objects.all()
        title = 'Логин'
        context= {'title':title,
        'form':form,
        }
        return render(request,'login.html',context)

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST or None)
        if form.is_valid():
            username= form.cleaned_data['username']
            password = form.cleaned_data['password']
            if '@' in username:
                user1= User.objects.filter(email=username).first()
                user= authenticate(username=user1,password=password)
            else:
                user= authenticate(username=username,password=password)
            if user:
                login(request,user)
            return HttpResponseRedirect('/')
        context={'form':form,}
        return render(request,'login.html',context)


class ProfileView(CusomerMixin,View):
    def get (self,request,*args,**kwargs):
        if not  request.user.is_authenticated:
            # messages.add_message(request,messages.ERROR,'Для просмотра заказов и их статуса зарегистрируйтесь')
            return redirect('registration')
        customer = self.get_customer()
        orders= Order.objects.filter(customer=customer).order_by('-created_at')
        title = 'Профиль: '+ request.user.username

        return render(request,'profile.html',{'title':title,
        'orders':orders,
 })


class ProductDetailView(DetailView):
    context_object_name='product'
    model= Product
    template_name='product_detail.html'
    slug_url_kwarg='slug'
    allow_empty=False

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        s=ProductFeatures.objects.filter(product=self.get_object()).first()
        items = Product.objects.filter(Q(features=s),~Q(title=self.get_object().title)).distinct()[:4]
        context['form'] = ReviewsForm(self.request.POST or None)
        context['items']=items
        context['title'] = self.get_object().title
        category=self.get_object().category
        return context


class CategorytDetailView(DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'
    allow_empty=False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        category = self.get_object()
        context['categories'] = self.model.objects.all()
        context['title']=self.get_object().name
        page_number = self.request.GET.get('page',1) 
        
        if not query and  not self.request.GET :
            print(' not querly')
            products= category.product_set.all().filter(available=True)
            paginator = Paginator(products,8)
            page =paginator.get_page(page_number) 
            context['category_products'] = page
            context['page']= page
            return context

        if query:
            print('querly')
            products = category.product_set.filter(Q(title__icontains=query),available=True)
            paginator = Paginator(products, 1)
            page =paginator.get_page(page_number) 
            context['category_products'] = page
            context['page']= page
            return context

        url_kwargs = {}
        if self.request.GET and not self.request.GET.get('page'):
            print('self')
            for item in self.request.GET:
                if len(self.request.GET.getlist(item)) > 1:
                    url_kwargs[item] = self.request.GET.getlist(item)
                else:
                    url_kwargs[item] = self.request.GET.get(item)
            q_condition_queries = Q()
            for key, value in url_kwargs.items():
                if isinstance(value, list):
                    q_condition_queries.add(Q(**{'value__in': value}), Q.OR)
                else:
                    q_condition_queries.add(Q(**{'value': value}), Q.OR)
            pf = ProductFeatures.objects.filter(
                q_condition_queries
            ).prefetch_related('product', 'feature').values('product_id')

            products = Product.objects.filter(id__in=[pf_['product_id'] for pf_ in pf],available=True)

            paginator = Paginator(products, 8)
            page =paginator.get_page(page_number) 
            context['category_products'] = page
            context['page']= page
            return context


class AddtoWhishlistView(View):
    def get(self,request,*args,**kwargs):
        product_slug= kwargs.get('slug')
        try:
            product= Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            try:
                return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
            except:
                return redirect('home')
        if request.user.is_authenticated:
            user = request.user
            # Whishlist.objects.get_or_create(owner=user,products=product)
            try:
                whish=Whishlist.objects.get(owner=user,products=product)
                if whish:
                    whish.delete()
            except Exception as e:
                new_whish = Whishlist(owner=user,products=product,whishlist=True)
                new_whish.save()
        else:
            name = str(request.session.session_key)
            # Whishlist.objects.get_or_create(session=name,products=product)
            try:
                whish=Whishlist.objects.get(session=name,products=product)
                if whish:
                    whish.delete()
            except Exception as e:
                new_whish = Whishlist(session=name,products=product,whishlist=True)
                new_whish.save()

        try:
            return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
        except:
            return redirect('home')

    

class WhislistView(ListView):
    model = Whishlist
    template_name='whishlist.html'
    context_object_name='favorite'
    paginate_by=9

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            favorite = Whishlist.objects.filter(owner=user)
        else:
            name = str(self.request.session.session_key)
            favorite = Whishlist.objects.filter(session=name)
        return favorite



class DeleteFromWhislist(View):

    def get(self,request,*args,**kwargs):

        product_slug=kwargs.get('slug')
        try:
            product= Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            try:
                return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
            except:
                return redirect('home')
        if request.user.is_authenticated:
            name = request.user
            user = User.objects.filter(username=name).first()
            try:
                Whishlist.objects.get(owner=user,products=product).delete()
            except Whishlist.DoesNotExist:
                return HttpResponseRedirect('/whishlist/')
        else:
            name = str(request.session.session_key)
            try:
                Whishlist.objects.get(session=name,products=product).delete()
            except Whishlist.DoesNotExist:
                return HttpResponseRedirect('/whishlist/')

        # messages.add_message(request,messages.INFO,'Товар удален из избранного')
        return HttpResponseRedirect('/whishlist/')


class SearchProduct(ListView):
    template_name = 'product-search.html'
    context_object_name = 'products'
    # allow_empty=False
    paginate_by = 9

    def get_queryset(self):
        search= self.request.GET.get('search')
        # print('поиск ',search)
        if search:
            if search[0].lower():
                search=search.title()
                products=Product.objects.filter(title__icontains=search,available=True)
                # print(products)
                return products

        else:
            try:
                return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
            except:
                return redirect('home')
    
    def get_context_data(self,*,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='Поиск по сайту: '+str(self.request.GET.get('search'))
        context['s']=f"s={self.request.GET.get('search')}&"
        return context


# class AllProducts(ListView):

#     template_name = 'products.html'
#     context_object_name = 'products'
#     # paginate_by = 9

#     return Product.objects.all()
    
#     def get_context_data(self,*,object_list=None,**kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title']='Все товары'
#         return context



class AllProducts(ListView):
    model = Product
    # queryset = Product.objects.filter(available=True)
    context_object_name = 'products'
    template_name = 'products.html'
    slug_url_kwarg = 'slug'
    allow_empty=False
    paginate_by=9
    extra_context = {'title':'Все товары'}

    def get_queryset(self, **kwargs):
        
        url_kwargs = {}
        if self.request.GET and not self.request.GET.get('page'):
            for item in self.request.GET:
                if len(self.request.GET.getlist(item)) > 1:
                    url_kwargs[item] = self.request.GET.getlist(item)
                else:
                    url_kwargs[item] = self.request.GET.get(item)
            if url_kwargs:
                
                q_condition_queries = Q()
                for key, value in url_kwargs.items():
                    if isinstance(value, list):
                        q_condition_queries.add(Q(**{'value__in': value}), Q.OR)
                    else:
                        q_condition_queries.add(Q(**{'value': value}), Q.OR)
                pf = ProductFeatures.objects.filter(
                    q_condition_queries
                ).prefetch_related('product', 'feature').values('product_id')
                products = Product.objects.filter(id__in=[pf_['product_id'] for pf_ in pf])
                return products
        else:
            products = Product.objects.all()
            return products


class AddReview(View):
    def post(self,request,id):
        if request.user.is_authenticated:
            try:
                product = Product.objects.get(id=id)
            except Product.DoesNotExist:
                try:
                    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
                except:
                    return redirect('home')
            last = product.rewiews_set.last()
            form=ReviewsForm(request.POST or None)
            if  form.is_valid() :
                form=form.save(commit=False)
                if last and form.revId == last.revId:
                    try:
                        return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
                    except:
                        return redirect('home')
                form.name = request.user.username
                form.product=product
                form.save()
            try:
                return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
            except:
                return redirect('home')
        else:
            return redirect('login')



class MakeOrderView(CusomerMixin,FinalPrice,View):
    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        cart = Cart(request)
        cart=cart.cart

        if bool(cart) is False:
            return redirect('home')

        price = self.get_final_price()
        title='Оформление заказа'
        context = {
            'title':title,
            'form': form
        }
        return render(request, 'checkout.html', context)


    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = self.get_customer()
        cart = Cart(request)
        cartdetail=cart.cart
        name=self.get_session_name()
        price = self.get_final_price()

        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.final_price=price
            new_order.save()

            for key,value in cartdetail.items():
                if name == value['userid']:
                    new= CartProduct.objects.create(
                    user=customer,
                    product=Product.objects.get(pk=value['product_id']),
                    size=value['size'],
                    price=value['price'],
                    )
                    new_order.cartproduct.add(new)
            new_order.customer.orders.add(new_order)
            cart.clear()

            if new_order.status_pay == 'online':
                new_order.status_online='Оплачено'
                new_order.save()

            subject = "Заказ на сайте 12312312"
            to = [new_order.email,]
            from_email = 'test@example.com'
            ctx = {
                'order': new_order,
            }
            message = get_template('message.html').render(ctx)
            msg = EmailMessage(subject, message, to=to, from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()
            # print(form.cleaned_data)
#             new_order.customer = customer
#             new_order.phone = form.cleaned_data['phone']

#             phone=form.cleaned_data['phone']

#             new_order.first_name = form.cleaned_data['first_name']

#             name=form.cleaned_data['first_name']

#             new_order.last_name = form.cleaned_data['last_name']
#             new_order.adress = form.cleaned_data['adress']

#             adress=form.cleaned_data['adress']

#             new_order.email=form.cleaned_data['email']
#             email = form.cleaned_data['email']

#             new_order.otdel = form.cleaned_data['otdel']
#             new_order.buying_type = form.cleaned_data['buying_type']
#             new_order.comment = form.cleaned_data['comment']
#             new_order.status_pay = 'nal'
#             comment=form.cleaned_data['comment']
#             payment = request.POST.get('payment')
#             if payment == 'online':
#                 new_order.status_pay = 'wait'
#                 new_order.save()
#                 self.cart.in_order = True
#                 self.cart.save()
#                 new_order.cart = self.cart
#                 new_order.save()
#                 customer.orders.add(new_order)

#                 subject = "Заказ на сайте 12312312 "
#                 to = [email,'zarj09@gmai.com']
#                 from_email = 'test@example.com'
#                 ctx = {
#                     'orders': orders,
#                 }
#                 message = get_template('message.html').render(ctx)
#                 msg = EmailMessage(subject, message, to=to, from_email=from_email)
#                 msg.content_subtype = 'html'
#                 msg.send()
#                 return redirect ('/pay/')

            
#             new_order.save()
#             self.cart.in_order = True
#             self.cart.save()
#             new_order.cart = self.cart
#             new_order.save()
#             customer.orders.add(new_order)
#             # orders = Order.objects.filter(customer=customer).order_by('-id')[:1]
# # -----------------------------------------------------------------------------------------------------------------------
# #             subject = "Заказ на сайте 12312312"
# #             to = [email,]
# #             from_email = 'test@example.com'
# #             ctx = {
# #                 'orders': orders,
# #             }
# #             message = get_template('message.html').render(ctx)
# #             msg = EmailMessage(subject, message, to=to, from_email=from_email)
# #             msg.content_subtype = 'html'
# #             msg.send()
# # # ----------------------------------------------------------------------------------------------------------------------


#             # messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


# def checkout(request):
#     form=OrderForm()
#     cart = Cart(request)
#     cart=cart.cart
#     if not cart:
#         return redirect('/')
#     return render(request, 'checkout.html',{'form':form})