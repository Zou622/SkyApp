from django.urls import path
from . import views

app_name = 'type_contrat'

urlpatterns = [
    path('type_contrat/', views.liste_type_contrat, name='liste_type'),
    path('type_contrat/ajouter/', views.ajouter_type_contrat, name='ajouter_type'),
    path('type_contrat/modifier/<int:type_id>/', views.modifier_type_contrat, name='modifier_type'),
    path('type_contrat/supprimer/<int:type_id>/', views.supprimer_type_contrat, name='supprimer_type'),
]