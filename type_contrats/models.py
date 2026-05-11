from django.db import models

# Create your models here.

class TypeContrat(models.Model):
    nom = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom