from django.urls import path
from . import views

app_name = 'base_stations'

urlpatterns = [
    path('base_stations/', views.liste_base_stations, name='liste_base_stations'),
    path('base_stations/ajouter/', views.ajouter_base_station, name='ajouter_base_station'),
    path('base_stations/modifier/<int:bs_id>/', views.modifier_base_station, name='modifier_base_station'),
    path('base_stations/supprimer/<int:bs_id>/', views.supprimer_base_station, name='supprimer_base_station'),
]