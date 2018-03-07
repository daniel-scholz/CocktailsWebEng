from django.http import HttpResponse, Http404
from django.shortcuts import render

# Create your views here.
from .models import Cocktail, Ingredient


def index(request):
    all_cocktails = Cocktail.objects.all()
    return render(request, 'cocktails/index.html',  {"all_cocktails":all_cocktails, })


def detail(request, id):
    try:
        cocktail = Cocktail.objects.get(pk = id)
        print(cocktail)

    except:
        raise Http404(" Cocktail %d not found" % (id))
    
    try:
        ingredients = Ingredient.objects.filter(cocktails = cocktail).all()
        print(ingredients)

    except:
        ingredients = ""

    return render(request, 'cocktails/detail.html',  {"cocktail":cocktail, "ingredients":ingredients, })
