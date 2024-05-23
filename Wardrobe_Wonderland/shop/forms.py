from django import forms
from .models import *

# class UserLoginForm(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password')
#
#
# class UserRegistrationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'username', 'password1', 'password2')


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


# class AddToFavoritesForm(forms.Form):
#     slug = forms.CharField(widget=forms.HiddenInput())
#     name = forms.CharField(widget=forms.HiddenInput())
#     image = forms.CharField(widget=forms.HiddenInput())
#     category = forms.CharField(widget=forms.HiddenInput())
#     price = forms.DecimalField(widget=forms.HiddenInput())
