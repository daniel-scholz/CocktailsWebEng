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
    cocktail = Cocktail.objects.filter(id=id).first()
    template = loader.get_template("cocktails/detail.html")
    print(template)
    context = {
        "cocktail": cocktail,
    }
    return HttpResponse(template.render(context, request))
