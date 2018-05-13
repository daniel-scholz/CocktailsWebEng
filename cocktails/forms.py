from typing import Optional

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from cocktails.models import Cocktail, Vote


# form for logging a user in or registering a users
class UserForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Username"}))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Password"}))

    class Meta:
        model = User
        fields = ['username', 'password']


class CocktailForm(ModelForm):
    # adds html attributes to the name and pictures
    name = forms.CharField(label="name", widget=forms.TextInput(
        attrs={'placeholder': 'Enter your cocktails name here..'}))
    picture = forms.ImageField(label="picture")

    class Meta:
        model = Cocktail
        fields = ['name', 'picture']

    # method for checking if a unit was valid
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

# specifying a vote form for catching up and down votes on the cocktails
class VoteForm(ModelForm):
    class Meta:
        model = Vote
        # determines the field for a vote form
        fields = ["voter", "cocktail", "is_upvote"]
