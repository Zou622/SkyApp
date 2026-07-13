from datetime import timedelta
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings

# SUPPRIMEZ cette ligne qui cause l'erreur
# from techniciens.models import Technicien

class User(AbstractUser):
    """Modèle utilisateur personnalisé"""

    # Types d'utilisateurs
    TYPE_USER = [
        ('admin', 'Administrateur'),
        ('superviseur', 'Superviseur'),
        ('commercial', 'Commercial'),
        ('technicien', 'Technicien'),
        ('comptable', 'Comptable'),
        ('rh', 'Ressources Humaines'),
    ]

    # Champs supplémentaires
    user_type = models.CharField(max_length=20, choices=TYPE_USER)

    # Lien vers le profil employé
    employe = models.OneToOneField(
        'employes.Employe',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_account'
    )

    # Dates
    date_inscription = models.DateTimeField(auto_now_add=True)
    derniere_connexion = models.DateTimeField(null=True, blank=True)

    # Statut
    est_actif = models.BooleanField(default=True)
    est_valide = models.BooleanField(default=False, help_text="Compte validé par un admin")

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        if self.employe:
            return f"{self.username} - {self.employe.nom} {self.employe.prenom} ({self.get_user_type_display()})"
        return f"{self.username} ({self.get_user_type_display()})"

    def get_full_name(self):
        if self.employe:
            return f"{self.employe.prenom} {self.employe.nom}"
        return self.username
    

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_tokens')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        """Le token est valide 1h seulement"""
        return not self.is_used and self.created_at >= timezone.now() - timedelta(hours=1)

    def mark_used(self):
        self.is_used = True
        self.save()