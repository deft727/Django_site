
from decimal import Decimal
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Max,Min

class Cart(object):

    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, action=None):
        """
        Add a product to the cart or update its quantity.
        """
        id = product.id
        newItem = True
        size = self.request.GET.get("size")
        # print(size,'iko')
        # if qty:
        #     qty=int(qty)
        # else:
        #     qty=1

        # else:
        #     size = 5
        x= product.sizes.all()
        maxsize=x.aggregate(Max('size'))['size__max']
        minsize=x.aggregate(Min('size'))['size__min']
        size = size if size else minsize
        if size:
            size=int(size)
        # print(product.price)
        # print(size)
        if str(product.id) not in self.cart.keys():

            self.cart[product.id] = {
                'userid': self.request.session.session_key,
                'product_id': id,
                'product_slug':product.slug,
                'name': product.title,
                'price': int(product.price*size),
                'image': product.image1.url,
                'size': size,
            }
        else:
            newItem = True

            for key, value in self.cart.items():
                if key == str(product.id):
                    if value['size']<maxsize:
                        value['size'] = (value['size'] + 5)  if size is None   else size
                    newItem = False
                    self.save()
                    break
            if newItem == True:

                self.cart[product.id] = {
                    'userid': self.request.session.session_key,
                    'product_id': product.id,
                    'name': product.title,
                    'size': size,
                    'price': int(product.price),
                    'image': product.image1.url,
                    'size':size
                }

        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrement(self, product):
        x= product.sizes.all()
        minsize=x.aggregate(Min('size'))['size__min']
        # print(minsize)
        for key, value in self.cart.items():
            if key == str(product.id):
                
                if(value['size'] > minsize) :
                    value['size'] = value['size'] - 5
                self.save()
                break
            else:
                print("Something Wrong")

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
