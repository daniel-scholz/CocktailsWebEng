# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import LoginForm, RegisterForm
from .models import Cocktail, Ingredient


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
