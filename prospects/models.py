from django.db import models
from commercials.models import Commercial

class Prospect(models.Model):
    commercial = models.ForeignKey(Commercial, on_delete=models.SET_NULL, null=True, blank=True)

    nom = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    quartier = models.CharField(max_length=100, blank=True, null=True)

    statut = models.CharField(
        max_length=20,
        choices=[
            ('nouveau', 'Nouveau'),
            ('en_cours', 'En cours'),
            ('converti', 'Converti'),
            ('perdu', 'Perdu'),
        ],
        default='nouveau'
    )

    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom