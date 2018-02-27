from django.http import HttpResponse


# Create your views here.


def index(request):
    TEXT_IO = open("cocktails/templates/cocktails/index.html")
    return HttpResponse(content=TEXT_IO)
