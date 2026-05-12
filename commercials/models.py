from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Commercial(models.Model):

    employe = models.OneToOneField(
        'employes.Employe',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commercial_profile'
    )

    SPECIALITES = [
        ('reseau', 'Réseau et Télécom'),
        ('vente', 'Vente et Marketing'),
        ('technique', 'Support Technique'),
        ('gestion', 'Gestion Clientèle'),
        ('autre', 'Autre'),
    ]

    specialite = models.CharField(
        max_length=50,
        choices=SPECIALITES,
        default='vente'
    )

    taux_commission = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    est_actif = models.BooleanField(default=True)

    class Meta:
        ordering = ['employe__nom', 'employe__prenom']

    def __str__(self):
        return f"{self.employe.prenom} {self.employe.nom}"