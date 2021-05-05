from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as authViews


urlpatterns = [
    path('',IndexView.as_view(),name='home'),
    path('product/<str:slug>/',ProductDetailView.as_view(), name='product_detail'),
    path('category_detail/<str:slug>/', CategorytDetailView.as_view(), name='category_detail'),
    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('cart/cart-detail/',cart_detail,name='cart_detail'),
    path('add-to-whishlist/<str:slug>/',AddtoWhishlistView.as_view(),name='add_to_whishlist'),
    path('whishlist/', WhislistView.as_view(),name='whishlist'),
    path('delete-favorite/<str:slug>/', DeleteFromWhislist.as_view(),name='delete_favorite'),
    path('search/',SearchProduct.as_view(),name='sear'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('registration/',RegistrationView.as_view(), name='registration'),
    path('login/',LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(next_page="/"), name='logout'),
    path('products/',AllProducts.as_view(),name='products'),
    path('addreview/<int:id>/',AddReview.as_view(),name='addreview'),
    path('checkout/',MakeOrderView.as_view(),name='make_order'),
            path('pass-reset/',authViews.PasswordResetView.as_view(template_name="pass-reset.html"),name="pass-reset"),
            path('passwod_reset_confirm/<uidb64>/<token>/',authViews.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),name="password_reset_confirm"),
            path('passwod-reset/done/',authViews.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),name="password_reset_done"),
            path('reset_password_complete/', authViews.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),name="password_reset_complete"),
    # path('review/<int:pk>/', ProductRewiew.as_view(),name="add_review"),
]


custom_404 = 'len_parfume.views.custom_404'
