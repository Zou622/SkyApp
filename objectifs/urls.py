from django.urls import path
from . import views

app_name = "objectifs"

urlpatterns = [
    # Liste des objectifs
    #path("", views.liste_objectif, name="liste_objectif"),
    # Ajouter un objectif
    path("ajouter/", views.ajouter_objectif, name="ajouter_objectif"),
    # Ajouter objectif depuis employé
    path("ajouter/<int:employe_id>/", views.ajouter_objectif, name="ajouter_objectif"),
    path("ajouter/<int:employe_id>/", views.ajouter_objectif, name="ajouter_objectif"),
    # Détail objectif
    path("detail/<int:pk>/", views.detail_objectif, name="detail_objectif"),
    # Modifier objectif
    path("modifier/<int:pk>/", views.modifier_objectif, name="modifier_objectif"),
    # Supprimer objectif
    path("supprimer/<int:pk>/", views.supprimer_objectif, name="supprimer_objectif"),
    ######################################
    path("", views.liste_objectifs, name="liste_objectif"),
    ###################################
    path("object/", views.get_objectifs_by_employe, name="ajax_objectifs"),
]
