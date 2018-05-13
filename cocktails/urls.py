from django.urls import path

from . import views

app_name = 'cocktails'

# all url patterns and their speicific views
# names store variables which could be used in the templates and views instead of the full url
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.UserFormView.as_view(), name='user'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('<int:pk>/', views.CocktailsDetailView.as_view(), name='detail'),
    path('cocktail/add', views.CocktailCreate.as_view(), name='cocktail-add'),
    path('<int:pk>/delete/', views.CocktailDelete.as_view(), name='cocktail-delete'),
    path("top5/", views.TopFiveView.as_view(), name="top-five"),
    path("a-to-z", views.AToZ.as_view(), name="a-to-z"),
    path("profile/<int:id>/", views.UserProfileView.as_view(), name="profile"),
    path("results", views.ResultView.as_view(), name="search-result"),
    path("shopping_list", views.ShoppingListView.as_view(), name="shopping-list"),
    path("vote/<int:id>", views.VoteView.as_view(), name="vote"),
]
