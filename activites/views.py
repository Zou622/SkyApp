from pyexpat import model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from collections import defaultdict
from django.contrib.auth.decorators import login_required, user_passes_test

from activites.models import Activite
from commercials.models import Commercial
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from datetime import date, datetime
from .models import Activite
from techniciens.models import Technicien
from .models import Client
from django.contrib.auth.decorators import login_required, user_passes_test


@csrf_exempt
@login_required
def activate_client(request, client_id):

    if request.method == 'POST':
        try:
            client = get_object_or_404(Client, id=client_id)

            # logique activation
            client.statut = "actif"   # 🔥 IMPORTANT: ton modèle utilise "statut", pas is_active
            client.save()

            return JsonResponse({
                'success': True,
                'message': f'Client {client.nom_client} activé avec succès'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'success': False,
        'message': 'Méthode non autorisée'
    }, status=405)


#Le module des cativités
@login_required
def ajouter_activite_avec_client(request, client_id):

    client = get_object_or_404(Client, id=client_id)
    techniciens = Technicien.objects.all().order_by('nom', 'prenom')

    if request.method == "POST":

        type_activite = request.POST.get("type_activite")
        date_activite = request.POST.get("date_activite")
        lieu = request.POST.get("lieu")
        description = request.POST.get("description")
        statut = request.POST.get("statut")
        heure_debut = request.POST.get("heure_debut") or None
        heure_fin = request.POST.get("heure_fin") or None

        technicien_ids = request.POST.getlist("techniciens")

        activite = Activite.objects.create(
            client=client,
            type_activite=type_activite,
            date_activite=date_activite,
            lieu=lieu,
            description=description,
            statut=statut,
            heure_debut=heure_debut,
            heure_fin=heure_fin,
        )

        # IMPORTANT pour ManyToMany
        activite.techniciens.set(technicien_ids)

        return redirect('detail_client', client_id=client_id)

    context = {
        "client": client,
        "techniciens": techniciens,
        "types_activite": Activite.TYPE_ACTIVITE_CHOICES,
        "statuts": Activite.STATUT_CHOICES,
        "aujourdhui": date.today().isoformat(),
    }

    return render(request, "clients/ajouter_activite_avec_client.html", context)


# clients/views.py
@login_required
def ajouter_activite(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        technicien_ids = request.POST.getlist('techniciens')
        type_activite = request.POST.get('type_activite')
        date_activite = request.POST.get('date_activite')
        heure_debut = request.POST.get('heure_debut')
        heure_fin = request.POST.get('heure_fin')
        description = request.POST.get('description', '').strip()
        lieu = request.POST.get('lieu', '').strip()
        statut = request.POST.get('statut', 'planifie')

        try:
            client = Client.objects.get(id=client_id)

            # 1️Créer l'activité SANS technicien
            activite = Activite.objects.create(
                client=client,
                type_activite=type_activite,
                date_activite=date_activite,
                heure_debut=heure_debut or None,
                heure_fin=heure_fin or None,
                description=description or None,
                lieu=lieu or None,
                statut=statut,
            )

            # Ajouter les techniciens après
            if technicien_ids:
                techniciens = Technicien.objects.filter(id__in=technicien_ids)
                activite.techniciens.set(techniciens)

            messages.success(
                request,
                f'Activité "{activite.get_type_activite_display()}" planifiée pour {client.nom_client}!'
            )

            return redirect('detail_client', client_id)

        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')

    clients = Client.objects.all().order_by('nom_client')
    techniciens = Technicien.objects.all().order_by('nom', 'prenom')

    return render(request, 'clients/ajouter_activite.html',{
        'clients': clients,
        'techniciens': techniciens,
        'types_activite': Activite.TYPE_ACTIVITE_CHOICES,
        'statuts': Activite.STATUT_CHOICES,
        'aujourdhui': date.today().isoformat(),
    })


@login_required
def list_activite(request):
    """Liste toutes les activités"""
    search_query = request.GET.get('search', '')
    statut_filter = request.GET.get('statut', '')
    type_filter = request.GET.get('type', '')
    date_filter = request.GET.get('date', '')

    activites_list = Activite.objects.all()

    # Filtre de recherche
    if search_query:
        activites_list = activites_list.filter(
            Q(client__nom_client__icontains=search_query) |
            Q(technicien__nom__icontains=search_query) |
            Q(technicien__prenom__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(lieu__icontains=search_query) |
            Q(notes__icontains=search_query)
        )

    # Filtre par statut
    if statut_filter:
        activites_list = activites_list.filter(statut=statut_filter)

    # Filtre par type d'activité
    if type_filter:
        activites_list = activites_list.filter(type_activite=type_filter)

    # Filtre par date
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            activites_list = activites_list.filter(date_activite=filter_date)
        except ValueError:
            pass

    # Tri
    activites_list = activites_list.order_by('-date_activite', 'heure_debut')

    # Pagination
    paginator = Paginator(activites_list, 5)
    page_number = request.GET.get('page')
    activites = paginator.get_page(page_number)

    # Statistiques
    aujourd_hui = date.today()
    stats = {
        'total': Activite.objects.count(),
        'aujourdhui': Activite.objects.filter(date_activite=aujourd_hui).count(),
        'planifie': Activite.objects.filter(statut='planifie').count(),
        'en_cours': Activite.objects.filter(statut='en_cours').count(),
        'termine': Activite.objects.filter(statut='termine').count(),
    }

    context = {
        'activites': activites,
        'search_query': search_query,
        'statut_filter': statut_filter,
        'type_filter': type_filter,
        'date_filter': date_filter,
        'stats': stats,
        'statuts': Activite.STATUT_CHOICES,
        'types_activite': Activite.TYPE_ACTIVITE_CHOICES,
    }
    return render(request, 'clients/list_activite.html', context)

@login_required
def calendrier_activites(request):
    """Vue calendrier des activités"""
    mois = request.GET.get('mois', date.today().month)
    annee = request.GET.get('annee', date.today().year)

    try:
        mois = int(mois)
        annee = int(annee)
    except ValueError:
        mois = date.today().month
        annee = date.today().year

    # Récupérer les activités du mois
    activites_mois = Activite.objects.filter(
        date_activite__year=annee,
        date_activite__month=mois
    ).order_by('date_activite')

    mois_noms_dict = {
        1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril', 5: 'Mai', 6: 'Juin',
        7: 'Juillet', 8: 'Août', 9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
    }

    context = {
        'activites': activites_mois,
        'mois': mois,
        'annee': annee,
        'mois_noms_dict': mois_noms_dict,
        'mois_range': range(1, 13),
    }

    return render(request, 'clients/calendrier_activites.html', context)

@login_required
def activites_aujourdhui(request):
    """Liste des activités du jour"""
    aujourdhui = date.today()
    activites = Activite.objects.filter(date_activite=aujourdhui).order_by('heure_debut')

    context = {
        'activites': activites,
        'date': aujourdhui,
    }
    return render(request, 'clients/activites_aujourdhui.html', context)


@login_required
def supprimer_activite(request, pk):
    """Supprimer une activité"""
    activite = get_object_or_404(Activite, pk=pk)

    if request.method == 'POST':
        client_nom = activite.client.nom_client
        activite.delete()
        messages.success(request, f'Activité pour {client_nom} supprimée avec succès!')
        return redirect('list_activite')

    context = {'activite': activite}
    return render(request, 'activites/supprimer_activite.html', context)




#la liste des activités par client
@login_required
def liste_activites_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    activites = Activite.objects.filter(client=client).order_by('-date_activite')

    context = {
        'client': client,
        'activites': activites,
    }

    return render(request, 'clients/liste_activites_client.html', context)



@login_required
def activites_par_technicien(request):
    date = timezone.now().date()
    activites = Activite.objects.filter(date_activite=date).prefetch_related('techniciens', 'client')

    techniciens_dict = defaultdict(list)

    for activite in activites:
        for tech in activite.techniciens.all():
            techniciens_dict[tech].append(activite)

    context = {
        'date': date,
        'techniciens_dict': dict(techniciens_dict)
    }

    return render(request, "activites_par_technicien.html", context)

@login_required
def mes_activites(request):

    if request.user.user_type != "technicien":
        return redirect("dashboard")  # sécurité

    # récupérer le technicien lié au user connecté
    technicien = request.user.technicien

    # filtrer seulement SES activités
    activites = Activite.objects.filter(technicien=technicien)

    context = {
        "activites": activites
    }

    return render(request, "activites/mes_activites.html", context)



# les fonctions de prospection
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import date

from clients.models import Client
from activites.models import Activite

def ajouter_prospection(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == "POST":
        try:
            activite = Activite.objects.create(
                client=client,
                type_activite='prospection',  # 🔥 FORCÉ
                date_activite=request.POST.get("date_activite"),
                lieu=request.POST.get("lieu"),
                description=request.POST.get("description"),
                statut=request.POST.get("statut"),
            )

            messages.success(request, "✅ Prospection enregistrée avec succès")
            return redirect('clients:detail_client', client.id)

        except Exception as e:
            messages.error(request, f"Erreur : {str(e)}")

    return render(request, "clients/ajouter_prospection.html", {
        "client": client,
        "statuts": Activite.STATUT_CHOICES,
        "aujourdhui": date.today().isoformat(),
    })


from django.db.models import Count
from activites.models import Activite


def liste_prospection(request):

    prospections = Activite.objects.filter(type_activite='prospection') \
        .select_related('client') \
        .order_by('-date_activite')

    # 🔥 STATISTIQUES
    stats = prospections.values('statut').annotate(total=Count('id'))

    stat_dict = {item['statut']: item['total'] for item in stats}

    context = {
        "prospections": prospections,
        "total": prospections.count(),
        "planifie": stat_dict.get('planifie', 0),
        "en_cours": stat_dict.get('en_cours', 0),
        "termine": stat_dict.get('termine', 0),
        "annule": stat_dict.get('annule', 0),
    }

    return render(request, "clients/liste_prospection.html", context)
    
    
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from activites.models import Activite


def modifier_prospection(request, id):
    prospection = get_object_or_404(
        Activite,
        id=id,
        type_activite='prospection'
    )

    if request.method == "POST":
        try:
            prospection.date_activite = request.POST.get("date_activite")
            prospection.lieu = request.POST.get("lieu")
            prospection.description = request.POST.get("description")
            prospection.statut = request.POST.get("statut")

            prospection.save()

            messages.success(request, "✅ Prospection modifiée avec succès")
            return redirect('activities:liste_prospection')

        except Exception as e:
            messages.error(request, f"Erreur : {str(e)}")

    return render(request, "clients/modifier_prospection.html", {
        "prospection": prospection,
        "statuts": Activite.STATUT_CHOICES
    })
    
    
    
    
    
    
    user = request.user

    # 🔐 rôle commercial
    is_commercial = hasattr(user, 'commercial_profile')

    # ================= BASE QUERY =================
    if is_commercial:
        prospects_list = Client.objects.filter(
            commercial=user.commercial_profile,
            type_client='prospect'
        )
    else:
        prospects_list = Client.objects.filter(
            type_client='prospect'
        )

    # ================= FILTRES =================
    search_query = request.GET.get('search')
    statut_filter = request.GET.get('statut')

    if search_query:
        prospects_list = prospects_list.filter(
            Q(nom_client__icontains=search_query) |
            Q(telephone__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    if statut_filter:
        prospects_list = prospects_list.filter(statut=statut_filter)

    # ================= STATS GENERALES =================
    total_prospects = prospects_list.count()

    statut_stats = {
        'actif': prospects_list.filter(statut='actif').count(),
        'suspendu': prospects_list.filter(statut='suspendu').count(),
        'resilie': prospects_list.filter(statut='resilie').count(),
        'non_actif': prospects_list.filter(statut='non_actif').count(),
    }

    def percent(part, total):
        return round((part / total) * 100, 1) if total else 0

    # ================= STATS ADMIN PAR COMMERCIAL =================
    commercial_stats = None
    if not is_commercial:
        commercial_stats = (
            prospects_list
            .values('commercial__id', 'commercial__nom', 'commercial__prenom')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

    # ================= PAGINATION =================
    paginator = Paginator(prospects_list.order_by('-id'), 10)
    page = request.GET.get('page')
    prospects = paginator.get_page(page)

    return render(request, 'clients/liste_prospection.html', {
        'prospects': prospects,
        'search_query': search_query,
        'statut_filter': statut_filter,

        'total_prospects': total_prospects,
        'statut_stats': statut_stats,

        'actif_percent': percent(statut_stats['actif'], total_prospects),
        'suspendu_percent': percent(statut_stats['suspendu'], total_prospects),
        'resilie_percent': percent(statut_stats['resilie'], total_prospects),

        'commercial_stats': commercial_stats,
        'is_commercial': is_commercial,
    })