from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from commercials.models import Commercial


class Client(models.Model):
    commercial = models.ForeignKey(Commercial, on_delete=models.SET_NULL, null=True)
    base_station = models.ForeignKey('base_stations.BaseStation', on_delete=models.SET_NULL, null=True)
    type_contrat = models.ForeignKey('type_contrats.TypeContrat', on_delete=models.SET_NULL, null=True)
    nom_client = models.CharField(max_length=255)
    adresse = models.TextField(blank=True, null=True)
    quartier = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    vlan = models.CharField(max_length=10, blank=True, null=True)
    adresse_ip = models.GenericIPAddressField(blank=True, null=True)
    statut = models.CharField(max_length=20, default='non_actif')
    capacite = models.CharField(max_length=5, blank=True, null=True)
    download = models.CharField(max_length=5, blank=True, null=True)
    upload = models.CharField(max_length=5, blank=True, null=True)
    contrat_pdf = models.FileField(upload_to='contrats/', blank=True, null=True)
    
    # 🔥 NOUVEAUX CHAMPS IMPORTANTS pour la coupure des connexions
    username_pppoe = models.CharField(max_length=100, blank=True, null=True)  # login MikroTik
    statut_paiement = models.CharField(max_length=20, default='impaye')  # payé / impayé
    date_expiration = models.DateField(blank=True, null=True)  # optionnel



    def __str__(self):
        return self.nom_client
    

    # Fonctions de vérification des rôles
    def est_technicien(user):
        return hasattr(user, 'technicien')

    def est_admin(user):
        return user.is_superuser or user.is_staff

