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
            "cotd": cocktails.get(pk=1)
        })


class TopFiveView(ListView):
    template_name = "cocktails/top_five.html"
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
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid() and form.units_valid(request.POST.getlist("unit")):
            cocktail = form.save(commit=False)
            ingredients = []
            ingredient_counter = int(request.POST["ingredient_counter"])
            for idx in range(ingredient_counter):
                ing = Ingredient()
                ing.name = request.POST.getlist("ingredient_name")[idx]
                ing.unit = request.POST.getlist("unit")[idx]
                ing.amount = float(request.POST.getlist("amount")[idx])
                ing.is_alcohol = True if request.POST.getlist("is_alcohol") else False
                ing.save()
                ingredients.append(ing)
            cocktail.creator = request.user
            form.save()
            cocktail.ingredient_set.set(ingredients)
            return redirect("cocktails:detail", cocktail.id)

        return render(request, self.template_name, {"form": form})


class CocktailUpdate(UpdateView):
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
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
