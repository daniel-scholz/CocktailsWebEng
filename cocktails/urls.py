from django.urls import path

from . import views

app_name = 'cocktails'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('<int:pk>/', views.IngredientsDetailView.as_view(), name='detail'),
    path('cocktail/add', views.CocktailCreate.as_view(), name='cocktail-add'),
    path('cocktail/<int:pk>', views.CocktailUpdate.as_view(), name='cocktail-update'),
    path('cocktail/<int:pk>/delete/', views.CocktailDelete.as_view(), name='cocktail-delete'),
]
