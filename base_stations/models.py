from django.db import models



class BaseStation(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom