from django.db import models
from employes.models import Employe
from employes.models import Employe


class Objectif(models.Model):

    employe = models.ForeignKey(
        "employes.Employe", on_delete=models.CASCADE, related_name="objectifs"
    )

    titre = models.CharField(max_length=200)

    description = models.TextField()

    date_debut = models.DateField()

    date_fin = models.DateField()

    pourcentage_realisation = models.IntegerField(default=0)

    statut = models.CharField(
        max_length=20,
        choices=[
            ("en_cours", "En cours"),
            ("termine", "Terminé"),
            ("retard", "En retard"),
        ],
        default="en_cours",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employe} - {self.titre}"
