from django.urls import path
from . import views

app_name = 'cocktails'

urlpatterns = [
    path('', views.index, name = 'index'), 
    path('<int:id>/', views.detail, name = 'detail'),
    path('<int:id>/favorite/', views.favorite, name = 'favorite'),
]
