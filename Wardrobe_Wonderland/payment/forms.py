from .models import *
from django import forms


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'email', 'street_address', 'apartment_address', 'country', 'city', 'zip']
        exclude = ['user', ]
