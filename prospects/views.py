from pyexpat.errors import messages

from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q, Count
from .models import Prospect
from commercials.models import Commercial



# liste des prospects
def list_prospects(request):
    user = request.user

<<<<<<< HEAD
    commercial = Commercial.objects.filter(employe__user_account=user).first()
=======
    commercial = Commercial.objects.filter(user_account=user).first()
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
    is_commercial = commercial is not None

    # ================= BASE QUERY =================
    if is_commercial:
        prospects_list = Prospect.objects.filter(commercial=commercial)
    else:
        prospects_list = Prospect.objects.all()

    # ❌ EXCLURE LES PROSPECTS CONVERTIS
    prospects_list = prospects_list.exclude(statut='converti')

    # ================= FILTRES =================
    search_query = request.GET.get('search', '')
    statut_filter = request.GET.get('statut', '')

    if search_query:
        prospects_list = prospects_list.filter(
            Q(nom__icontains=search_query) |
            Q(telephone__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # ⚠️ IMPORTANT
    # On garde statut_filter MAIS converti est déjà exclu automatiquement
    if statut_filter:
        prospects_list = prospects_list.filter(statut=statut_filter)

    # ================= STATS =================
    total_prospects = prospects_list.count()

    statut_stats = {
        'nouveau': prospects_list.filter(statut='nouveau').count(),
        'en_cours': prospects_list.filter(statut='en_cours').count(),
        'converti': prospects_list.filter(statut='converti').count(),  # sera toujours 0 maintenant
        'perdu': prospects_list.filter(statut='perdu').count(),
    }

    def percent(part, total):
        return round((part / total) * 100, 1) if total else 0

    # ================= ADMIN STATS =================
    commercial_stats = None
    if not is_commercial:
        commercial_stats = (
            prospects_list
<<<<<<< HEAD
            .values('commercial__id', 'commercial__employe__nom', 'commercial__employe__prenom')
=======
            .values('commercial__id', 'commercial__nom', 'commercial__prenom')
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
            .annotate(total=Count('id'))
            .order_by('-total')
        )

    return render(request, 'prospects/list_prospects.html', {
        'prospects': prospects_list.order_by('-id'),
        'search_query': search_query,
        'statut_filter': statut_filter,

        'total_prospects': total_prospects,
        'statut_stats': statut_stats,

        'nouveau_percent': percent(statut_stats['nouveau'], total_prospects),
        'en_cours_percent': percent(statut_stats['en_cours'], total_prospects),
        'converti_percent': percent(statut_stats['converti'], total_prospects),

        'commercial_stats': commercial_stats,
        'is_commercial': is_commercial,
    })
    

# ajout d'un prospect
def add_prospect(request):

    commercials = Commercial.objects.all()
    is_commercial = request.user.user_type == "commercial"

    # 🔥 récupérer le commercial connecté
    commercial_connecte = None
    if is_commercial:
<<<<<<< HEAD
        commercial_connecte = Commercial.objects.filter(employe__user_account=request.user).first()
=======
        commercial_connecte = Commercial.objects.filter(user_account=request.user).first()
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad

    if request.method == "POST":

        nom = request.POST.get("nom")
        telephone = request.POST.get("telephone")
        email = request.POST.get("email")
        quartier = request.POST.get("quartier")
        adresse = request.POST.get("adresse")
        statut = request.POST.get("statut")

        # 🔥 logique importante ici
        if is_commercial:
            commercial_id = commercial_connecte.id if commercial_connecte else None
        else:
            commercial_id = request.POST.get("commercial") or None

        try:
            Prospect.objects.create(
                nom=nom,
                telephone=telephone,
                email=email,
                quartier=quartier,
                adresse=adresse,
                statut=statut,
                commercial_id=commercial_id
            )

            messages.success(request, "Prospect ajouté avec succès !")
            return redirect("prospects:list_prospects")

        except Exception as e:
            messages.error(request, f"Erreur : {str(e)}")

    return render(request, "prospects/add_prospect.html", {
        "commercials": commercials,
        "statuts": Prospect._meta.get_field("statut").choices,
        "is_commercial": is_commercial
    })
    
     
    
# détail d'un prospect
def detail_prospect(request, id):
    prospect = get_object_or_404(Prospect, id=id)
    return render(request, "prospects/detail_prospect.html", {"prospect": prospect})


# édition d'un prospect
def edit_prospect(request, id):
    prospect = get_object_or_404(Prospect, id=id)
    commercials = Commercial.objects.all()
    statuts = Prospect._meta.get_field("statut").choices  # Défini une fois

    if request.method == "POST":
        prospect.nom = request.POST.get("nom")
        prospect.telephone = request.POST.get("telephone")
        prospect.email = request.POST.get("email")
        prospect.quartier = request.POST.get("quartier")
        prospect.adresse = request.POST.get("adresse")
        prospect.statut = request.POST.get("statut")
        prospect.commercial_id = request.POST.get("commercial") or None

        prospect.save()
        messages.success(request, 'Prospect modifié avec succès!')
        return redirect("prospects:list_prospects")

    return render(request, "prospects/add_prospect.html", {
        "prospect": prospect,
        "commercials": commercials,
        "statuts": statuts,  # Utilisé ici
    })


# suppression d'un prospect
def delete_prospect(request, id):
    prospect = get_object_or_404(Prospect, id=id)
    
    if request.method == "POST":
        # Suppression via POST (confirmation SweetAlert)
        prospect_name = prospect.nom
        prospect.delete()
        messages.success(request, f"Le prospect '{prospect_name}' a été supprimé avec succès !")
        return redirect("prospects:list_prospects")
    
    # Pour GET, retourner une confirmation (optionnel)
    return render(request, "prospects/confirm_delete.html", {"prospect": prospect})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from prospects.models import Prospect
from clients.models import Client


@login_required
def convertir_prospect_en_client(request, prospect_id):
    prospect = get_object_or_404(Prospect, id=prospect_id)

    # 🔥 Vérifie s'il n'est pas déjà converti
    if prospect.statut == "converti":
        messages.warning(request, "Ce prospect est déjà converti.")
        return redirect('prospects:list_prospects')

    # =========================
    # 1. CRÉATION CLIENT
    # =========================
    Client.objects.create(
        nom_client=prospect.nom,
        telephone=prospect.telephone,
        email=prospect.email,
        adresse=prospect.adresse,
        quartier=prospect.quartier,
        commercial=prospect.commercial,
        statut='non_actif'
    )

    # =========================
    # 2. UPDATE PROSPECT
    # =========================
    prospect.statut = "converti"
    prospect.save()

    messages.success(request, "Prospect converti en client avec succès !")
    return redirect('prospects:list_prospects')