from django.urls import path
from . import views

app_name = 'base_stations'

urlpatterns = [
    path('', views.liste_base_stations, name='liste_base_stations'),
    path('ajouter/', views.ajouter_base_station, name='ajouter_base_station'),
    path('modifier/<int:bs_id>/', views.modifier_base_station, name='modifier_base_station'),
    path('supprimer/<int:bs_id>/', views.supprimer_base_station, name='supprimer_base_station'),
]