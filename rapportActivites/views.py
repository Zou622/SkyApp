from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime

from activites.views import Q
from .models import Activite, RapportActivite
from .forms import RapportActiviteForm
from techniciens.models import Technicien
from clients.models import Client

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from activites.models import Activite


from django.shortcuts import render, get_object_or_404, redirect
from .forms import RapportActiviteForm
from activites.models import Activite


#La liste des activté par technicien
@login_required
def liste_activites_technicien(request, technicien_id=None):

    if not technicien_id:
        # Si pas d'ID, prendre le premier technicien
        technicien = Technicien.objects.first()
    else:
        try:
            technicien = Technicien.objects.get(id=technicien_id)
        except Technicien.DoesNotExist:
            return render(request, 'erreur.html', {
                'message': f"Technicien avec ID {technicien_id} non trouvé."
            })

    if not technicien:
        return render(request, 'erreur.html', {
            'message': "Aucun technicien dans la base de données."
        })

    activites = Activite.objects.filter(techniciens=technicien)

    return render(request, 'clients/mes_activites.html', {
        'activites': activites,
        'technicien': technicien,
    })

from django.utils import timezone



#La vue pour demarrer une activité
@login_required
def demarrer_activite(request, activite_id):
    """Permet au technicien de démarrer une activité"""

    activite = get_object_or_404(Activite, id=activite_id)

    try:
        technicien = Technicien.objects.get(user=request.user)
    except Technicien.DoesNotExist:
        messages.error(request, "Vous n'êtes pas enregistré comme technicien")
        return redirect('rapportActivites:liste_activites_technicien')

    if technicien not in activite.techniciens.all():
        messages.error(request, "Vous n'êtes pas affecté à cette activité")
        return redirect('rapportActivites:liste_activites_technicien')

    if activite.statut != 'planifie':
        messages.warning(request, "Cette activité a déjà démarré ou est terminée")
        return redirect('rapportActivites:liste_activites_technicien')

    activite.statut = 'en_cours'
    activite.heure_debut = timezone.now().time()
    activite.save()

    messages.success(request,
                     f"✅ Activité démarrée : {activite.get_type_activite_display()} chez {activite.client.nom_client}")
    return redirect('liste_activites_technicien')



@login_required
def creer_rapport(request, activite_id):

    activite = get_object_or_404(Activite, id=activite_id)

    # 🔒 empêcher double rapport (OneToOne)
    if hasattr(activite, 'rapport'):
        return redirect('clients:modifier_rapport', activite.rapport.id)

    # 🔥 récupérer technicien connecté
    try:
        technicien = Technicien.objects.get(user=request.user)
    except Technicien.DoesNotExist:
        messages.error(request, "Aucun technicien associé à votre compte. Contactez l'administrateur.")
        return redirect('clients:mes_activites')

    if request.method == "POST":

        form = RapportActiviteForm(
            request.POST,
            request.FILES,
            activite=activite
        )

        if form.is_valid():
            rapport = form.save(commit=False)

            # 🔥 relations importantes
            rapport.activite = activite
            rapport.technicien = technicien

            rapport.save()

            # ✅ mettre activité en terminé
            activite.statut = "termine"
            activite.save()

            return redirect('rapportActivites:liste_activites_technicien')

    else:
        form = RapportActiviteForm(activite=activite)

    return render(request, "rapportsActivites/creer_rapport.html", {
        "form": form,
        "activite": activite
    })
    
    
    
    
def detail_rapport(request, rapport_id):

    rapport = get_object_or_404(RapportActivite, id=rapport_id)

    type_activite = rapport.activite.type_activite.lower().strip()

    champs_par_type = {

        "installation": [
            'date_intervention_reelle',
            'heure_debut_reelle',
            'heure_fin_reelle',
            'description',
            'travaux_realises',
            'equipements_utilises',
            'parametres_configures',
            'photo_avant',
            'photo_apres'
        ],

        "maintenance": [
            'date_intervention_reelle',
            'heure_debut_reelle',
            'heure_fin_reelle',
            'travaux_realises',
            'materiel_remplace',
            'solutions_apportees',
            'photo_avant',
            'photo_apres',
            'description'
        ],

        "survey": [
            'date_intervention_reelle',
            'heure_debut_reelle',
            'heure_fin_reelle',
            'travaux_realises',
            'etat_avant',
            'difficultes_rencontrees',
            'photo_avant',
            'description'
        ],

        "investigation": [
            'date_intervention_reelle',
            'heure_debut_reelle',
            'heure_fin_reelle',
            'travaux_realises',
            'difficultes_rencontrees',
            'solutions_apportees'
        ],

        "tirage_fo": [
            'date_intervention_reelle',
            'heure_debut_reelle',
            'heure_fin_reelle',
            'point_de_depart',
            'nombre_de_joinbox_poser',
            'type_de_brain',
            'photo_apres',
        ],

        "raccordement": [
            'date_intervention_reelle',
            'heure_debut_reelle',
            'heure_fin_reelle',
            'quel_joinbox',
            'tube',
            'quel_brain',
            'photo_avant',
            'photo_apres',
            'description'
        ],

        "remplacement": [
            'date_intervention_reelle',
            'heure_debut_reelle',
            'heure_fin_reelle',
            'description',
            'photo_avant',
            'photo_apres'
        ],

        "noc support": [
            'date_intervention_reelle',
            'heure_debut_reelle',
            'heure_fin_reelle',
            'description',
            'plainte_client',
            'photo_ping',
            'photo_appareils_connecte'
        ],

        "autre": [
            'date_intervention_reelle',
            'heure_debut_reelle',
            'heure_fin_reelle',
            'description',
            'travaux_realises',
            'difficultes_rencontrees',
            'solutions_apportees',
            'photo_avant',
            'photo_apres'
        ]
    }

    champs = champs_par_type.get(type_activite, [])

    return render(request, "rapportActivites/detail_rapport.html", {
        "rapport": rapport,
        "champs": champs
    })
    
    


def liste_rapports(request):
    rapports = RapportActivite.objects.select_related(
        'activite', 'activite__client'
    ).order_by('-id')

    # 🔍 Recherche
    search = request.GET.get('search')
    if search:
        rapports = rapports.filter(
            Q(activite__client__nom_client__icontains=search) |
            Q(activite__type_activite__icontains=search)
        )

    # 🎯 Filtre par date
    date = request.GET.get('date')
    if date:
        rapports = rapports.filter(date_intervention_reelle=date)

    return render(request, 'rapportsActivites/liste_rapports.html', {
        'rapports': rapports
    })
