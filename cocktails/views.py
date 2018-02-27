from django.http import HttpResponse

# Create your views here.
from .models import Cocktail


def index(request):
    all = Cocktail.objects.all()
    html = "<h1> list of all cocktails</h1> "
    for a in all:
        html += "<a href='/cocktails/%d/'>%s </a> <br>" % (a.id, a.name)
    return HttpResponse(html)


def detail(request, id):
    return HttpResponse("Details for Cocktail %d" % id)
