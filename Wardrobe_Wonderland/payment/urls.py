from django.urls import path
from .views import *
from .webhooks import stripe_webhook
app_name = 'payment'

urlpatterns = [
    path('payment_success/', payment_success, name='payment_success'),
    path('payment_failed/', payment_failed, name='payment_failed'),
    path('shipping/', shipping, name='shipping'),
    path('checkout/', checkout, name='checkout'),
    path('my_orders/', user_orders, name='user_orders'),
    path('complete_order/', complete_order, name='complete_order'),
    path('webhook_stripe/', stripe_webhook, name='webhook_stripe'),
    path("order/<int:order_id>/pdf/", admin_order_pdf, name="admin_order_pdf"),
]

