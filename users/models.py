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
<<<<<<< HEAD
        ('rh', 'Ressources Humaines'),
=======
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
    ]

    # Champs supplémentaires
    user_type = models.CharField(max_length=20, choices=TYPE_USER)
<<<<<<< HEAD

    # Lien vers le profil employé
    employe = models.OneToOneField(
        'employes.Employe',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_account'
    )
=======
    nom = models.CharField(max_length=25, blank=True)
    prenom = models.CharField(max_length=30, blank=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    adresse = models.TextField(blank=True)
    photo = models.ImageField(upload_to='users/photos/', null=True, blank=True)
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad

    # Dates
    date_inscription = models.DateTimeField(auto_now_add=True)
    derniere_connexion = models.DateTimeField(null=True, blank=True)

    # Statut
    est_actif = models.BooleanField(default=True)
    est_valide = models.BooleanField(default=False, help_text="Compte validé par un admin")

<<<<<<< HEAD
=======
    # Utilisez des chaînes de caractères au lieu d'importer les classes
    technicien = models.OneToOneField(
        'techniciens.Technicien',  # Changé ici
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_account'
    )

    commercial = models.OneToOneField(
        'commercials.Commercial',  # Changé ici aussi si nécessaire
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commercial_profile'
    )

>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
<<<<<<< HEAD
        if self.employe:
            return f"{self.username} - {self.employe.nom} {self.employe.prenom} ({self.get_user_type_display()})"
        return f"{self.username} ({self.get_user_type_display()})"

    def get_full_name(self):
        if self.employe:
            return f"{self.employe.prenom} {self.employe.nom}"
        return self.username
=======
        return f"{self.username} - {self.get_full_name()} ({self.get_user_type_display()})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
    

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