# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from cocktails.models import Cocktail, Ingredient


class IndexView(ListView):
    template_name = "cocktails/index.html"
    context_object_name = 'all_cocktails'

    def get_queryset(self):
        return Cocktail.objects.all()


class IngredientsDetailView(DetailView):
    model = Cocktail
    template_name = "cocktails/detail.html"

    def get_context_data(self, **kwargs):
        context = super(IngredientsDetailView, self).get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.filter(cocktail=self.object.id)
        # print(context)
        return context


class CocktailCreate(CreateView):
    model = Cocktail
    fields = ["name", "picture"]  # , "ingredient_set"]


class CocktailUpdate(UpdateView):
    model = Cocktail
    fields = ["name", "picture"]  # , "ingredient_set"]

class CocktailDelete(DeleteView):
    model = Cocktail
    success_url = reverse_lazy("cocktails:index")
