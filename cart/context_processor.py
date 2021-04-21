from .cart import Cart


def cart_total_amount(request):
	# if request.user.is_authenticated:
	cart = Cart(request)
	total_bill = 0
	for key,value in request.session['cart'].items():
		total_bill = total_bill + (int(value['price']) )
		# print(int(value['price']) , int(value['size']))
	return {'cart_total_amount' : total_bill} 
	# else:
	# 	return {'cart_total_amount' : 0} 

