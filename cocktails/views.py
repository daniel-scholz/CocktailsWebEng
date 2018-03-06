from django.http import HttpResponse
from django.template import loader

# Create your views here.
from .models import Cocktail


def index(request):
    all_cocktails = Cocktail.objects.all()
    context = {
        "all_cocktails": all_cocktails,
    }
    template = loader.get_template('cocktails/index.html')
    return HttpResponse(template.render(context, request))


def detail(request, id):
    c = Cocktail.objects.filter(id=id)
    template = loader.get_template("cocktails/detail.html")
    context = {
        "cocktail": c,
    }
    return HttpResponse(template.render(context, request))
