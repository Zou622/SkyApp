from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

from .models import Employe


@receiver(post_save, sender=Employe)
def create_or_update_employe_profile(sender, instance, created, **kwargs):
    """Créer le profil Commercial ou Technicien automatiquement à partir de la fonction."""
    Commercial = apps.get_model('commercials', 'Commercial')
    Technicien = apps.get_model('techniciens', 'Technicien')

    if instance.fonction == 'commercial':
        if hasattr(instance, 'technicien_profile') and instance.technicien_profile is not None:
            instance.technicien_profile.delete()

        Commercial.objects.get_or_create(
            employe=instance,
            defaults={
                'taux_commission': 10.00,
                'est_actif': True,
            }
        )

    elif instance.fonction == 'technicien':
        if hasattr(instance, 'commercial_profile') and instance.commercial_profile is not None:
            instance.commercial_profile.delete()

        Technicien.objects.get_or_create(
            employe=instance,
            defaults={
                'statut': 'actif',
                'est_actif': True,
            }
        )

    else:
        if hasattr(instance, 'commercial_profile') and instance.commercial_profile is not None:
            instance.commercial_profile.delete()
        if hasattr(instance, 'technicien_profile') and instance.technicien_profile is not None:
            instance.technicien_profile.delete()
