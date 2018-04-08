# Create your views here.

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

from .forms import LoginForm, RegisterForm, CocktailForm
from .models import Cocktail, Ingredient


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
            sort_param = self.request.GET["sort_by"]
        else:
            sort_param = "taste"
        return Cocktail.objects.all().order_by("-%s_rating" % sort_param)[:5]


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
        results = Cocktail.objects.filter(name__contains=q).order_by(Lower("name"))
        q = " _ " if q == "" else q
        return render(request, self.template_name, {"cocktails": results, "q": q})


class ShoppingListView(View):
    template_name = "cocktails/shopping-list.html"
    context_object_name = "items"

    def get(self, request):
        return render(request, self.template_name,
                      {"items": Ingredient.objects.filter(on_shopping_list=True).order_by(Lower("name"))})

    def post(self, request):
        shopping_list = Ingredient.objects.filter(on_shopping_list=True)
        if request.POST["cocktail"]:
            shopping_list = shopping_list.filter(cocktail=request.POST["cocktail"])

        print("shopping list:", shopping_list)
        for key in request.POST:
            print(key, request.POST.getlist(key))
            try:
                ingredient = Ingredient.objects.get(pk=key)
                ingredient.on_shopping_list = True
                shopping_list = shopping_list.exclude(id=ingredient.id)
                ingredient.save()
            except:
                print("%s is not found in ingredient database" % key)
        for ingredient in shopping_list:
            ingredient.on_shopping_list = False
            ingredient.save()

        return redirect("cocktails:shopping-list")


class CocktailsDetailView(DetailView):
    model = Cocktail
    template_name = "cocktails/detail.html"

    def get_context_data(self, **kwargs):
        context = super(CocktailsDetailView, self).get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.filter(
            cocktail=self.object.id)
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
                ing.is_alcohol = True if request.POST.getlist("is_not_alcohol")[idx] == "0" else False
                ing.save()
                ingredients.append(ing)
            cocktail.creator = request.user

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
                cocktail.drunk_rating = (alc_sum / liq_sum) * 5
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
        kwargs["ing"] = Ingredient.objects.filter(cocktail_id=kwargs["pk"])
        print(kwargs)
        # return render(request, self.form_class(), context)
        return super(CocktailUpdate, self).get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super(CocktailUpdate, self).get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.filter(
            cocktail=self.object.id)
        return context


class CocktailDelete(DeleteView):
    model = Cocktail
    success_url = reverse_lazy("cocktails:index")


# authentication stuff
class UserFormView(View):
    form_class = RegisterForm
    template_name = "cocktails/registration_form.html"

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)
        print(form)
        if form.is_valid():
            # fake, validation commit
            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            passwd = form.cleaned_data["password"]

            user.set_password(passwd)
            user.save()

            # returns User objects if credentials r correct
            user = authenticate(username=username, password=passwd)

            if user and user.is_active:
                login(request, user)
                return redirect("cocktails:index")
        return render(request, self.template_name, {"form": form})


class LoginFormView(View):
    form_class = LoginForm
    template_name = "cocktails/login_form.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
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
