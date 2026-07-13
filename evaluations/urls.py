from django.urls import path
from . import views

app_name = "evaluations"

urlpatterns = [
    path("", views.liste_evaluations, name="liste_evaluations"),
    path("ajouter/", views.ajouter_evaluation, name="ajouter_evaluation"),
    path(
        "evaluations/modifier/<int:pk>/",
        views.modifier_evaluation,
        name="modifier_evaluation",
    ),
    path("detail/<int:pk>/", views.detail_evaluation, name="detail_evaluation"),
    path(
        "supprimer/<int:pk>/", views.supprimer_evaluation, name="supprimer_evaluation"
    ),
]
