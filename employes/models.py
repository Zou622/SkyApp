from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Departement(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Poste(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Employe(models.Model):

    SEXE = (
        ("Homme", "Homme"),
        ("Femme", "Femme"),
    )

    STATUT = (
        ("Actif", "Actif"),
        ("Inactif", "Inactif"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    matricule = models.CharField(max_length=50, unique=True)

    photo = models.ImageField(upload_to="employes/photos/", null=True, blank=True)

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    sexe = models.CharField(max_length=10, choices=SEXE)

    date_naissance = models.DateField(null=True, blank=True)

    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    adresse = models.TextField(blank=True)

    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True)

    poste = models.ForeignKey(Poste, on_delete=models.SET_NULL, null=True)

    date_embauche = models.DateField()

    statut = models.CharField(max_length=20, choices=STATUT, default="Actif")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
