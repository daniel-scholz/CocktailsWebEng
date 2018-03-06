from django.contrib import admin

# Register your models here.
from cocktails.models import Cocktail, Ingredient

admin.site.register(Cocktail)
admin.site.register(Ingredient)
