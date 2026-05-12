from django.db import models
from django.conf import settings

# SUPPRIMEZ cette ligne si elle existe
# from users.models import User

class Technicien(models.Model):
    employe = models.OneToOneField(
        'employes.Employe',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='technicien_profile'
    )

    # Informations professionnelles
    specialite = models.CharField(
        max_length=100,
        verbose_name="Spécialité",
        blank=True,
        null=True
    )

    # Statut
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('congé', 'En congé'),
        ('mission', 'En mission'),
    ]
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='actif',
        verbose_name="Statut"
    )
    est_actif = models.BooleanField(default=True)

    # Dates
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employe.nom} {self.employe.prenom}"

    def nom_complet(self):
        return f"{self.employe.nom} {self.employe.prenom}"

    def get_photo_url(self):
        if self.employe.photo and hasattr(self.employe.photo, 'url'):
            return self.employe.photo.url
        return '/static/images/default-avatar.png'

    class Meta:
        verbose_name = "Technicien"
        verbose_name_plural = "Techniciens"
        ordering = ['employe__nom', 'employe__prenom']