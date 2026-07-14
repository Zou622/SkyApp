from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Commercial(models.Model):

<<<<<<< HEAD
    employe = models.OneToOneField(
        'employes.Employe',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commercial_profile'
=======
    user_account = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="commercial_profile"
    )

    SPECIALITES = [
        ('reseau', 'Réseau et Télécom'),
        ('vente', 'Vente et Marketing'),
        ('technique', 'Support Technique'),
        ('gestion', 'Gestion Clientèle'),
        ('autre', 'Autre'),
    ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    quartier = models.CharField(max_length=100, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    specialite = models.CharField(
        max_length=50,
        choices=SPECIALITES,
        default='vente'
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
    )

    taux_commission = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

<<<<<<< HEAD
=======
    date_embauche = models.DateField(blank=True, null=True)

>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    est_actif = models.BooleanField(default=True)

    class Meta:
<<<<<<< HEAD
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
=======
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
