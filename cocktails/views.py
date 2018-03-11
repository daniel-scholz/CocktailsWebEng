from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Cocktail, Ingredient


def index(request):
    all_cocktails = Cocktail.objects.all()
    return render(request, 'cocktails/index.html',  {"all_cocktails":all_cocktails, })


def detail(request, id):
    cocktail = get_object_or_404(Cocktail, pk = id)

    try:
        ingredients = Ingredient.objects.filter(cocktails = cocktail).all()
        print(ingredients)

    except:
        ingredients = ""

    return render(request, 'cocktails/detail.html',  {"cocktail":cocktail, "ingredients":ingredients, })


def favorite(request, id):
    cocktail = get_object_or_404(Cocktail, pk = id)
    try:
        selected_ingredient = Ingredient.objects.get(pk = request.POST['ingredient'])
        print("selected ingredient:%s" % selected_ingredient.name)
                
        for key in request.POST.lists():

            ##################################################
            print("%s %s" % (key.index(key[1]), " abc"))

    except(KeyError, Ingredient.DoesNotExist):
        return render(request, 'cocktails/detail.html',  {
            "cocktail":cocktail, 
            "error_message":"you're dumb", 
        })


    try:
        ingredients = Ingredient.objects.filter(cocktails = cocktail).all()
        print(ingredients)

    except:
        ingredients = ""

    selected_ingredient.is_alcohol = not selected_ingredient.is_alcohol
    selected_ingredient.save()
    return render(request, 'cocktails/detail.html',  {"cocktail":cocktail, "ingredients":ingredients, })

    