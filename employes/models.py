from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


<<<<<<< HEAD
=======
class Departement(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
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

<<<<<<< HEAD
    matricule = models.CharField(max_length=50, unique=True, blank=True)

    @property
    def has_user_account(self):
        """Vérifie si l'employé a un compte utilisateur actif."""
        try:
            return self.user_account is not None and self.user_account.est_actif
        except:
            return False
=======
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    matricule = models.CharField(max_length=50, unique=True)
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad

    photo = models.ImageField(upload_to="employes/photos/", null=True, blank=True)

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    sexe = models.CharField(max_length=10, choices=SEXE)

    date_naissance = models.DateField(null=True, blank=True)

    telephone = models.CharField(max_length=20)
<<<<<<< HEAD
    email = models.EmailField(blank=True, null=True)

    adresse = models.TextField(blank=True, null=True)
    quartier = models.CharField(max_length=100, blank=True, null=True)

    FONCTIONS = [
        ('commercial', 'Commercial'),
        ('technicien', 'Technicien'),
    ]

    fonction = models.CharField(
        max_length=20,
        choices=FONCTIONS,
        null=True,
        blank=True,
    )

    date_embauche = models.DateField(null=True, blank=True)
=======
    email = models.EmailField(blank=True)

    adresse = models.TextField(blank=True)

    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True)

    poste = models.ForeignKey(Poste, on_delete=models.SET_NULL, null=True)

    date_embauche = models.DateField()
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad

    statut = models.CharField(max_length=20, choices=STATUT, default="Actif")

    created_at = models.DateTimeField(auto_now_add=True)

<<<<<<< HEAD
    def save(self, *args, **kwargs):
        if not self.matricule:
            # Générer automatiquement le matricule basé sur l'ID
            super().save(*args, **kwargs)  # Sauvegarder d'abord pour avoir un ID
            self.matricule = f"EMP{self.id:04d}"
            super().save(update_fields=['matricule'])  # Sauvegarder seulement le matricule
        else:
            super().save(*args, **kwargs)

=======
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
    def __str__(self):
        return f"{self.nom} {self.prenom}"
