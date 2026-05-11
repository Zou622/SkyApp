from django.urls import path
from . import views

urlpatterns = [
    path("", views.liste_employes, name="liste_employes"),
    path("ajouter/", views.ajouter_employe, name="ajouter_employe"),
]
