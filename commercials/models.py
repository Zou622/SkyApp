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
        if self.employe:
            return f"{self.employe.prenom} {self.employe.nom}"
        return "Commercial sans employé"

    # Propriétés pour accéder aux champs de l'employé
    @property
    def nom(self):
        return self.employe.nom if self.employe else ""

    @property
    def prenom(self):
        return self.employe.prenom if self.employe else ""

    @property
    def email(self):
        return self.employe.email if self.employe else ""

    @property
    def telephone(self):
        return self.employe.telephone if self.employe else ""

    @property
    def adresse(self):
        return self.employe.adresse if self.employe else ""

    @property
    def quartier(self):
        return self.employe.quartier if self.employe else ""

    @property
    def date_embauche(self):
        return self.employe.date_embauche if self.employe else None

    @property
    def prenom(self):
        return self.employe.prenom if self.employe else ''

    @property
    def nom(self):
        return self.employe.nom if self.employe else ''