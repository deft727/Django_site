from .models import User,Customer
from cart.cart import Cart


class CusomerMixin:
    
    def get_customer(self):
        if self.request.user.is_authenticated:
            customer = Customer.objects.filter(user=self.request.user).first()
            if not customer:
                customer = Customer.objects.create(user=self.request.user)
            return customer

        name = str(self.request.session.session_key)
        user= User.objects.filter(username=name).first()
        if not user:
            user = User.objects.create_user(name, 'randomemail', 'randomemail')
        customer = Customer.objects.filter(user=user).first()
        if not customer:
            customer= Customer.objects.create(
                    user=user 
                )
        return customer
    
    def get_session_name(self):
        name = str(self.request.session.session_key)
        if name:
            return name
        else:
            request.session.create()


class FinalPrice:

    def get_final_price(self):
        cart = Cart(self.request)
        total_bill = 0
        for key,value in self.request.session['cart'].items():
            total_bill = total_bill + (int(value['price']))
        return total_bill