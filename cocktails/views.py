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
from extra_views import InlineFormSet

from .forms import LoginForm, RegisterForm, CocktailForm, IngredientForm
from .models import Cocktail, Ingredient


class IndexView(ListView):
    template_name = "cocktails/index.html"
    context_object_name = 'all_cocktails'

    def get_queryset(self):
        """query_set = QuerySet()
        query_set += Cocktail.objects.all()
        query_set += Cocktail.objects.get(pk=random.random(len(Cocktail.objects.all())))
        return query_set
"""
        return Cocktail.objects.all()


class TopFiveView(ListView):
    template_name = "cocktails/top-five.html"
    context_object_name = "cocktails"

    def get_queryset(self):
        return Cocktail.objects.all().order_by("drunk_scale")[:5]


class AToZ(ListView):
    template_name = "cocktails/a-to-z.html"
    context_object_name = "cocktails"

    def get_queryset(self):
        return Cocktail.objects.all().order_by(Lower("name"))


class CocktailsDetailView(DetailView):
    model = Cocktail
    template_name = "cocktails/detail.html"

    def get_context_data(self, **kwargs):
        context = super(CocktailsDetailView, self).get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.filter(cocktail=self.object.id)
        return context


class UserProfileView(View):
    template_name = "cocktails/user-profile.html"

    def get(self, request, id):
        return render(request, template_name=self.template_name, context={
            "cocktails": Cocktail.objects.filter(creator=id),
            "other_user": User.objects.filter(pk=id).first()
        })


# Cocktail creating and updating and stuff
class IngredientInline(InlineFormSet):
    model = Ingredient
    fields = "__all__"


@method_decorator(login_required, name='dispatch')
class CocktailCreate(CreateView):
    form_class = CocktailForm
    template_name = "cocktails/cocktail_form.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            cocktail = form.save(commit=False)
            ingredients = []
            for i in request.POST.getlist("ingredients"):
                ingredients.append(Ingredient.objects.get(pk=i))
            cocktail.creator = request.user
            form.save()
            cocktail.ingredient_set.set(ingredients)
            return redirect("cocktails:detail", cocktail.id)

        return render(request, self.template_name, {"form": form})


class IngredientCreate(CreateView):
    form_class = IngredientForm
    template_name = "cocktails/cocktail_form.html"

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        # picture = request.POST["picture"]
        form = self.form_class(request.POST, request.FILES)
        print(form.clean())
        if form.is_valid() and form.clean():
            ingredient = form.save(commit=False)
            # ingredient.ingredient_set = Ingredient.objects.filter(ingredient=ingredient)

            form.save()
            cocktail = Cocktail.objects.get(pk=ingredient.cocktail.id)
            return redirect("cocktails:detail", cocktail.id)

        return render(request, self.template_name, {"form": form})


class CocktailUpdate(UpdateView):
    model = Cocktail
    fields = ["name", "picture"]  # , "ingredient_set"]


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
