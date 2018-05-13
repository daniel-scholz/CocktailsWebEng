from django.contrib import admin

# Register your models here.
from cocktails.models import Cocktail, Ingredient, Vote

# add models to manage them in a admin view
admin.site.register(Cocktail)
admin.site.register(Ingredient)
admin.site.register(Vote)
