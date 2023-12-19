from django.urls import path
from .views import *

urlpatterns = [
    path('', CategoryListView.as_view(), name='category'),
    path('registration/', registration, name='registration_page'),
    path('login/', login, name='login_page'),
    path('cart/', view_cart, name='cart_view_page'),
    path('profile/', profile, name='profile_page'),
    path('logout/', logout_view, name='logout'),
    path('warn/', cart_warning, name='cart_warning_page'),
    path('search/', Search.as_view(), name='search_results'),
    path('items/', ItemListView.as_view(), name='item_list'),
    path('items/<slug:slug>/', ItemDetailView.as_view(), name='item_detail'),
    path('add_to_favorites/', add_to_favorites, name='add_to_favorites'),
    path('favorites/', favorite, name='favorites'),
    path('remove_from_favorites/', remove_from_favorites, name='remove_from_favorites'),
    # path('favorites/', favorites, name='favorites_page'),
    # path('payment_form/', payment_form, name='payment_form'),
    # path('payment_successful/', payment_successful, name='payment_successful'),
    # path('payment_cancelled/', payment_cancelled, name='payment_cancelled'),
    # path('stripe_webhook/', stripe_webhook, name='stripe_webhook')
]

