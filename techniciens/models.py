from django.db import models
from django.conf import settings

# SUPPRIMEZ cette ligne si elle existe
# from users.models import User

class Technicien(models.Model):
<<<<<<< HEAD
    employe = models.OneToOneField(
        'employes.Employe',
=======
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    email = models.EmailField(verbose_name="Email", unique=True, blank=True, null=True)
    telephone = models.CharField(max_length=20, verbose_name="Téléphone" , blank=True, null=True)

    # Adresse
    quartier = models.CharField(max_length=100, verbose_name="Quartier", blank=True, null=True)
    adresse = models.TextField(verbose_name="Adresse complète" , blank=True, null=True)

    # Photo
    photo = models.ImageField(
        upload_to='techniciens/photos/',
        verbose_name="Photo",
        blank=True,
        null=True
    )

    # Informations professionnelles
    specialite = models.CharField(
        max_length=100,
        verbose_name="Spécialité",
        blank=True,
        null=True
    )

    # Relation vers User (optionnelle - si vous voulez aussi un lien depuis Technicien)
    user = models.OneToOneField(
        'users.User',  # Utilisez une chaîne de caractères
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='technicien_profile'
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
<<<<<<< HEAD
=======
    date_embauche = models.DateField(verbose_name="Date d'embauche" , blank=True, null=True)
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
<<<<<<< HEAD
        return f"{self.employe.nom} {self.employe.prenom}"

    @property
    def nom(self):
        return self.employe.nom if self.employe else ''

    @property
    def prenom(self):
        return self.employe.prenom if self.employe else ''

    @property
    def email(self):
        return self.employe.email if self.employe else ''

    @property
    def telephone(self):
        return self.employe.telephone if self.employe else ''

    @property
    def adresse(self):
        return self.employe.adresse if self.employe else ''

    @property
    def quartier(self):
        return self.employe.quartier if self.employe else ''

    @property
    def date_embauche(self):
        return self.employe.date_embauche if self.employe else None

    def nom_complet(self):
        return f"{self.employe.nom} {self.employe.prenom}"

    def get_photo_url(self):
        if self.employe and self.employe.photo and hasattr(self.employe.photo, 'url'):
            return self.employe.photo.url
=======
        return f"{self.nom} {self.prenom}"

    def nom_complet(self):
        return f"{self.nom} {self.prenom}"

    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
        return '/static/images/default-avatar.png'

    class Meta:
        verbose_name = "Technicien"
        verbose_name_plural = "Techniciens"
<<<<<<< HEAD
        ordering = ['employe__nom', 'employe__prenom']
=======
        ordering = ['nom', 'prenom']
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
