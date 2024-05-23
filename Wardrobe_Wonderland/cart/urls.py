from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', cart_view, name='cart_view'),
    path('cart/add/', cart_add, name='add_to_cart'),
    path('cart/delete/', cart_delete, name='delete_from_cart'),
    path('cart/update/', cart_update, name='update_cart'),
]
