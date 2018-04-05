from django.urls import path

from . import views

app_name = 'cocktails'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('<int:pk>/', views.CocktailsDetailView.as_view(), name='detail'),
    path('cocktail/add', views.CocktailCreate.as_view(), name='cocktail-add'),
    path('cocktail/<int:pk>', views.CocktailUpdate.as_view(), name='cocktail-update'),
    path('cocktail/<int:pk>/delete/', views.CocktailDelete.as_view(), name='cocktail-delete'),
    path("top5/", views.TopFiveView.as_view(), name="top-five"),
    path("a-to-z", views.AToZ.as_view(), name="a-to-z"),
    path("profile/<int:id>/", views.UserProfileView.as_view(), name="profile"),
    path("results", views.ResultView.as_view(), name="search-result")
]
