from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from cocktails.models import Cocktail, Ingredient


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
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all())

    class Meta:
        model = Cocktail
        fields = ['name', 'picture', "ingredients"]  # TODO add , 'ingredient'] to Cocktail Creation Form


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'weight', "quantity", "volume",
                  "is_alcohol", "cocktail"]

    def clean(self):
        super(IngredientForm, self).clean()
        return self.fields[2] or self.fields[3] or self.fields[1]
