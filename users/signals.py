from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def update_employe_on_user_save(sender, instance, **kwargs):
    """
    Quand un utilisateur est désactivé (soft delete), 
    on met aussi à jour l'employe si nécessaire.
    """
    if instance.employe:
        # Si le compte est désactivé, on peut garder la relation
        # Le bouton "Créer un compte" dépendra de has_user_account qui vérifie est_actif
        pass


@receiver(pre_delete, sender=User)
def cleanup_employe_on_user_delete(sender, instance, **kwargs):
    """
    Quand un utilisateur est complètement supprimé,
    on nettoie la relation avec l'employe.
    """
    if instance.employe:
        # La relation sera déjà rompue par le CASCADE automatique de Django
        # Mais on peut ajouter de la logique ici si nécessaire
        pass
