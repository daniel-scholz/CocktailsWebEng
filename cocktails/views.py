# Create your views here.
import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView

from .forms import UserForm, RegisterForm, CocktailForm, VoteForm
from .models import Cocktail, Ingredient, Vote


class IndexView(View):
    template_name = "cocktails/index.html"

    def get(self, request):
        cocktails = Cocktail.objects
        return render(request, template_name=self.template_name, context={
            "all_cocktails": cocktails.all(),
            "cotd": cocktails.get(name="Daniel is in fact making progress")
        })


class TopFiveView(ListView):
    template_name = "cocktails/top_five.html"
    context_object_name = "cocktails"

    def get_queryset(self):
        if self.request.GET.__contains__("sort_by") and self.request.GET["sort_by"] != "":
            sort_param = "-" + self.request.GET["sort_by"] + "_rating" if self.request.GET[
                                                                              "sort_by"] != "latest" else "timestamp"
        else:
            sort_param = "timestamp"
        return Cocktail.objects.all().order_by("%s" % sort_param)[:5]


class AToZ(ListView):
    template_name = "cocktails/a_to_z.html"
    context_object_name = "cocktails"

    def get_queryset(self):
        return Cocktail.objects.all().order_by(Lower("name"))


class ResultView(ListView):
    template_name = "cocktails/search_results.html"
    context_object_name = "cocktails"

    def get(self, request, *args, **kwargs):
        q = request.GET['q']
        results = Cocktail.objects.filter(
            name__contains=q).order_by(Lower("name"))
        q = " _ " if q == "" else q
        return render(request, self.template_name, {"cocktails": results, "q": q})


@method_decorator(login_required, name='dispatch')
class ShoppingListView(View):
    template_name = "cocktails/shopping-list.html"
    context_object_name = "items"

    def get(self, request):
        print(Ingredient.objects.filter(on_shopping_list_of=request.user))
        return render(request, self.template_name,
                      {"items": Ingredient.objects.filter(on_shopping_list_of=request.user).order_by(Lower("name"))})

    def post(self, request):
        # get shopping list of logged in user
        shopping_list = Ingredient.objects.filter(on_shopping_list_of=request.user)

        print("shopping list:", shopping_list)

        for item in request.POST.getlist("on_shopping_list"):
            try:
                key, value = item.split(":")
                print(key, value)
                ingredient = Ingredient.objects.get(pk=key)
                ingredient.on_shopping_list_of = request.user if "True" == value else None
                ingredient.save()
            except:
                print("%s is not found in ingredient database" % item)

        return redirect("cocktails:shopping-list")


class CocktailsDetailView(DetailView):
    model = Cocktail
    template_name = "cocktails/detail.html"

    def get_context_data(self, **kwargs):
        context = super(CocktailsDetailView, self).get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.filter(
            cocktail=self.object.id)
        votes = Cocktail.objects.get(pk=self.object.id).vote_set.all()
        for vote in votes:
            if self.request.user == vote.voter:
                context["votable"] = "up" if vote.is_upvote else "down"
                return context

        return context


class UserProfileView(View):
    template_name = "cocktails/user_profile.html"

    def get(self, request, id):
        return render(request, template_name=self.template_name, context={
            "cocktails": Cocktail.objects.filter(creator=id),
            "other_user": User.objects.filter(pk=id).first()
        })


@method_decorator(login_required, name='dispatch')
class CocktailCreate(CreateView):
    form_class = CocktailForm
    template_name = "cocktails/cocktail_form.html"

    def post(self, request, *args, **kwargs):
        # id = kwargs["pk"]
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid() and form.units_valid(request.POST.getlist("unit")):
            cocktail = form.save(commit=False)
            ingredients = []
            counter = request.POST["ingredient_counter"]
            ingredient_counter = int(counter) if counter else 0
            for idx in range(ingredient_counter):
                ing = Ingredient()
                ing.name = request.POST.getlist("ingredient_name")[idx]
                ing.unit = request.POST.getlist("unit")[idx]
                ing.amount = float(request.POST.getlist("amount")[idx])
                ing.is_alcohol = True if request.POST.getlist(
                    "is_not_alcohol")[idx] == "0" else False
                ing.save()
                ingredients.append(ing)
            cocktail.creator = request.user
            cocktail.timestamp = datetime.date.today
            form.save()
            cocktail.ingredient_set.set(ingredients)
            alc_sum = 0
            liq_sum = 0
            ingredient_set = ingredients
            for i in ingredient_set:
                amount = i.amount
                unit: str = i.unit
                factor = unit.split("l")[0]
                if factor == "m":
                    scale = 0.001
                elif factor == "c":
                    scale = 0.01
                elif factor == "d":
                    scale = 0.1
                else:
                    scale = 1
                amount *= scale
                if i.is_alcohol:
                    alc_sum += amount
                liq_sum += amount
            if liq_sum != 0:
                cocktail.drunk_rating = (alc_sum / liq_sum) * 10
            else:
                cocktail.drunk_rating = 0
            cocktail.save()
            return redirect("cocktails:detail", cocktail.id)

        return render(request, self.template_name, {"form": form})


@method_decorator(login_required, name='dispatch')
class CocktailUpdate(UpdateView):
    model = Cocktail
    fields = ["name", "picture"]

    # form_class = CocktailForm

    def get(self, request, *args, **kwargs):
        if request.user == Cocktail.objects.get(pk=kwargs["pk"]).creator:
            kwargs["ing"] = Ingredient.objects.filter(cocktail_id=kwargs["pk"])
            print(kwargs)
            # return render(request, self.form_class(), context)

            return super(CocktailUpdate, self).get(request, args, kwargs)

        return redirect('cocktails:detail', kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super(CocktailUpdate, self).get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.filter(
            cocktail=self.object.id)
        return context


@method_decorator(login_required, name='dispatch')
class CocktailDelete(DeleteView):
    model = Cocktail
    success_url = reverse_lazy("cocktails:index")


class UserFormView(View):
    form_class = UserForm
    template_name = "cocktails/user_form.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if "register" in request.POST:
            # fake, validation commit
            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data["password"]

            user.set_password(password)
            user.save()
        else:
            username = request.POST["username"]
            password = request.POST["password"]
        # returns User objects if credentials r correct
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect("cocktails:index")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("cocktails:index")


@method_decorator(login_required, name='dispatch')
class VoteView(View):

    def get(self, id):
        return redirect("cocktails:detail", id)

    def post(self, request, id):
        v = Vote()
        v.voter = request.user
        v.is_upvote = True if request.POST["vote"] == "up" else False
        cocktail = Cocktail.objects.get(pk=id)
        v.cocktail = cocktail
        v.save()
        cocktail.taste_rating = len(Vote.objects.filter(cocktail=id, is_upvote=True)) - len(
            Vote.objects.filter(cocktail=id,
                                is_upvote=False))
        cocktail.save()
        return redirect("cocktails:detail", id)
