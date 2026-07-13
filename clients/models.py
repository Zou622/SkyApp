from datetime import timezone

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from commercials.models import Commercial


class Client(models.Model):
    FORFAIT_CHOICES = [
        ('didié', 'Didié'),
        ('partagé', 'Partagé'),
    ]

    commercial = models.ForeignKey('commercials.Commercial', on_delete=models.SET_NULL, null=True)
    base_station = models.ForeignKey('base_stations.BaseStation', on_delete=models.SET_NULL, null=True)
    type_contrat = models.ForeignKey('type_contrats.TypeContrat', on_delete=models.SET_NULL, null=True)
    forfait = models.CharField(max_length=50, blank=True, null=True, choices=FORFAIT_CHOICES)  
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



    # Champs pour soft delete
    est_supprime = models.BooleanField(default=False)
    date_suppression = models.DateTimeField(null=True, blank=True)
    
    def soft_delete(self):
        """Marque le client comme supprimé sans le supprimer vraiment"""
        self.est_supprime = True
        self.date_suppression = timezone.now()
        self.statut = 'resilie'
        self.save()
    
    def restaurer(self):
        """Restaure un client supprimé"""
        self.est_supprime = False
        self.date_suppression = None
        self.save()

    # 🔥 SYSTEM

    username_pppoe = models.CharField(max_length=100, blank=True, null=True)
    statut_paiement = models.CharField(max_length=20, default='impaye')
    date_expiration = models.DateField(blank=True, null=True)
    
    # Les méthodes pour les classes de badge en fonction du statut et du type d'activité
    def statut_badge_class(self):
        return {
        "en_attente": "bg-info",
        "planifie": "bg-primary",
        "en_cours": "bg-warning text-dark",
        "termine": "bg-success",
        "annule": "bg-danger",
    }.get(self.statut, "bg-secondary")


    def type_badge_class(self):
        return {
        "noc support": "bg-dark",
        "installation": "bg-info",
        "maintenance": "bg-primary",
    }.get(self.type_activite, "bg-secondary")

    def __str__(self):
        return self.nom_client