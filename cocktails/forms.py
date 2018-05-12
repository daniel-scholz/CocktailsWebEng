from typing import Optional

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from cocktails.models import Cocktail, Vote


class RegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Username"}))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Password"}))

    class Meta:
        model = User
        fields = ['username', 'password']


class CocktailForm(ModelForm):
    # query_set = Ingredient.objects.order_by("name").values_list("name").distinct()
    # ingredients = forms.ModelMultipleChoiceField(queryset=query_set)
    name = forms.CharField(label="name", widget=forms.TextInput(
        attrs={'placeholder': 'Enter your cocktails name here..'}))
    picture = forms.ImageField(label="picture")
    # widget=forms.FileInput(attrs={'onchange': 'readURL(this)'}))

    class Meta:
        model = Cocktail
        fields = ['name', 'picture']

    def units_valid(self, units) -> (bool, Optional[str]):
        valid_units = ["ml", "cl", "dl", "l", "stk"]
        check = False
        if not units:
            return True
        for u in units:
            check = False
            for v in valid_units:
                if u.lower() == v:
                    check = True
                    break
            if not check:
                self.add_error("name",
                               ValueError(
                                   "Allowed Units for ingredients are: %s" % valid_units.__str__().strip(
                                       "[")
                                   .strip("]")))
                return False

        return check


class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ["voter", "cocktail", "is_upvote"]
