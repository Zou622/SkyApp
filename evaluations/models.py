from django.db import models
from django.conf import settings
from employes.models import Employe
from objectifs.models import Objectif


class Evaluation(models.Model):

    employe = models.ForeignKey(
        Employe,
        on_delete=models.CASCADE,
        related_name="evaluations_objectifs",  # Nom unique
    )

    # NOUVEAU
    objectif = models.ForeignKey(
        Objectif,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evaluations",
    )

    evaluateur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    date_evaluation = models.DateField(auto_now_add=True)

    ponctualite = models.IntegerField(default=0)

    discipline = models.IntegerField(default=0)

    performance = models.IntegerField(default=0)

    commentaire = models.TextField(blank=True)

    score_total = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        p = float(self.ponctualite or 0)
        d = float(self.discipline or 0)
        pr = float(self.performance or 0)

        self.score_total = (p + d + pr) / 3

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.employe}"
