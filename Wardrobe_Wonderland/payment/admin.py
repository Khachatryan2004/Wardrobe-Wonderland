from django.contrib import admin
from .models import *

admin.site.register(ShippingAddress)
admin.site.register(OrderItem)
admin.site.register(Order)