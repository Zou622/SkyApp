from django.urls import path
from . import views

app_name = 'employes'

urlpatterns = [
    path("", views.liste_employes, name="liste_employes"),
    path("ajouter/", views.ajouter_employe, name="ajouter_employe"),
    path("<int:employe_id>/", views.detail_employe, name="detail_employe"),
    path("<int:employe_id>/modifier/", views.modifier_employe, name="modifier_employe"),
    path("<int:employe_id>/creer-compte/", views.creer_compte_utilisateur, name="creer_compte_utilisateur"),
    path("departements/", views.liste_departements, name="liste_departements"),
    path("departements/ajouter/", views.ajouter_departement, name="ajouter_departement"),
    path("departements/<int:departement_id>/supprimer/", views.supprimer_departement, name="supprimer_departement"),
    path("postes/", views.liste_postes, name="liste_postes"),
    path("postes/ajouter/", views.ajouter_poste, name="ajouter_poste"),
    path("postes/<int:poste_id>/supprimer/", views.supprimer_poste, name="supprimer_poste"),
]
