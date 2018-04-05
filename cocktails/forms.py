from typing import Optional

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
    # query_set = Ingredient.objects.order_by("name").values_list("name").distinct()
    # ingredients = forms.ModelMultipleChoiceField(queryset=query_set)
    class Meta:
        model = Cocktail
        fields = ['name', 'picture']  # , "ingredients"]  # TODO add , 'ingredient'] to Cocktail Creation Form

    def units_valid(self, units) -> (bool, Optional[str]):
        valid_units = ["ml", "cl", "dl", "l", "stk"]
        check = False
        for u in units:
            check = False
            for v in valid_units:
                if u.lower() == v:
                    check = True
                    break
            if check == False:
                self.add_error("name",
                               ValueError(
                                   "Allowed Units for ingredients are:" + valid_units.__str__().strip("[").strip("]")))
                return False

        return check


"""
class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'weight', "quantity", "volume",
                  "is_alcohol", "cocktail"]

    def clean(self):
        super(IngredientForm, self).clean()
        return self.fields[2] or self.fields[3] or self.fields[1]
"""
