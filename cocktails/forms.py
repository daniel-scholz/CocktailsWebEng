from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from cocktails.models import Cocktail


class RegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class CocktailForm(ModelForm):
    class Meta:
        model = Cocktail
        fields = ['name', 'picture']  # TODO add , 'ingredient'] to Cocktail Creation Form
