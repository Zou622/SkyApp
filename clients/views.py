from pyexpat import model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from collections import defaultdict
from django.contrib.auth.decorators import login_required, user_passes_test
from activites.models import Activite  # ✅ OK - import depuis l'app activites
from base_stations.models import BaseStation
from commercials.models import Commercial
from django.urls import reverse
from django.core.exceptions import ValidationError 
from django.contrib import messages
from django.db.models import Q
from datetime import date, datetime
from django.core.validators import validate_ipv46_address
from rapportActivites.forms import RapportActiviteForm
from rapportActivites.models import RapportActivite
from techniciens.models import Technicien
from type_contrats.models import TypeContrat
from .models import Client  # ✅ OK - import depuis le même app
from users.models import User
from django.core.exceptions import PermissionDenied
from .decorators import technicien_required, role_required, admin_required



def is_allowed_roles(roles):
    def check(user):
        return user.is_authenticated and user.user_type in roles
    return user_passes_test(check)


@login_required
@is_allowed_roles(['admin', 'superviseur'])
def afficher_formulaire_ajout(request):
    # Récupérer tous les commerciaux
    commerciaux = Commercial.objects.all()
    base_stations = BaseStation.objects.all()
    type_contrats = TypeContrat.objects.all()
    client = None  # Aucun client existant lors de l'ajoutbase

    return render(request, 'clients/Add_client.html', {
        'commerciaux': commerciaux,
        'base_stations': base_stations,
        'type_contrats': type_contrats,
        'client': client
    })

@login_required
@is_allowed_roles(['admin', 'superviseur'])
def enregistrer_client(request):
    if request.method == 'POST':

        nom_client = request.POST.get('nom_client', '').strip()
        adresse = request.POST.get('adresse', '').strip()
        quartier = request.POST.get('quartier', '').strip()
        telephone = request.POST.get('telephone', '').strip()
        email = request.POST.get('email', '').strip()

        vlan = request.POST.get('vlan', '').strip()
        adresse_ip = request.POST.get('adresse_ip', '').strip()

        statut = request.POST.get('statut', 'non_actif').strip()

        capacite = request.POST.get('capacite', '').strip()
        download = request.POST.get('download', '').strip()
        upload = request.POST.get('upload', '').strip()

        contrat_pdf = request.FILES.get('contrat_pdf')
        
        # ================= NOUVEAU CHAMP FORFAIT =================
        forfait = request.POST.get('forfait', '').strip()

        # ================= COMMERCIAL =================
        commercial = None
        commercial_id = request.POST.get('commercial_id')

        if commercial_id:
            try:
                commercial = Commercial.objects.get(id=commercial_id)
            except Commercial.DoesNotExist:
                pass

        # ================= TYPE CONTRAT =================
        type_contrat = None
        type_contrat_id = request.POST.get('type_contrat_id')

        if type_contrat_id:
            try:
                type_contrat = TypeContrat.objects.get(id=type_contrat_id)
            except TypeContrat.DoesNotExist:
                pass

        # ================= BASE STATION =================
        base_station = None
        base_station_id = request.POST.get('base_station')

        if base_station_id:
            try:
                base_station = BaseStation.objects.get(id=base_station_id)
            except BaseStation.DoesNotExist:
                pass

        # ================= CREATE =================
        Client.objects.create(
            nom_client=nom_client,
            adresse=adresse,
            quartier=quartier,
            telephone=telephone,
            email=email,

            vlan=vlan or None,
            adresse_ip=adresse_ip or None,

            statut=statut,

            type_contrat=type_contrat,
            base_station=base_station,

            capacite=capacite or None,
            download=download or None,
            upload=upload or None,
            
            forfait=forfait or None,  

            contrat_pdf=contrat_pdf,
            commercial=commercial
        )

        # 🔥 MESSAGE DIFFÉRENT
        messages.success(request, f'✅ Client "{nom_client}" ajouté avec succès!')
        return redirect('clients:list_client')

    return redirect('clients:afficher_formulaire')


@login_required
@is_allowed_roles(['admin', 'superviseur','commercial'])
def list_client(request):
    user = request.user

    # 🔐 Détection du commercial (CORRECT)
<<<<<<< HEAD
    commercial = Commercial.objects.filter(employe__user_account=user).first()
=======
    commercial = Commercial.objects.filter(user_account=user).first()
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
    is_commercial = commercial is not None

    # ================= BASE QUERY =================
    # 🔥 FILTRER UNIQUEMENT LES CLIENTS NON SUPPRIMÉS (est_supprime=False)
    if is_commercial:
        clients_list = Client.objects.filter(commercial=commercial, est_supprime=False)
    else:
        clients_list = Client.objects.filter(est_supprime=False)

    # ================= FILTRES =================
    search_query = request.GET.get('search', '')
    statut_filter = request.GET.get('statut', '')

    if search_query:
        clients_list = clients_list.filter(
            Q(nom_client__icontains=search_query) |
            Q(telephone__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    if statut_filter:
        clients_list = clients_list.filter(statut=statut_filter)

    # ================= STATS =================
    total_clients = clients_list.count()
    actif_count = clients_list.filter(statut='actif').count()
    suspendu_count = clients_list.filter(statut='suspendu').count()
    resilie_count = clients_list.filter(statut='resilie').count()
    non_actif_count = clients_list.filter(statut='non_actif').count()

    def percentage(part, total):
        return round((part / total) * 100, 1) if total > 0 else 0

    actif_pourcentage = percentage(actif_count, total_clients)
    suspendu_pourcentage = percentage(suspendu_count, total_clients)
    resilie_pourcentage = percentage(resilie_count, total_clients)
    non_actif_pourcentage = percentage(non_actif_count, total_clients)

    # ================= PAGINATION =================
    paginator = Paginator(clients_list.order_by('-id'), 10)
    page = request.GET.get('page')
    clients = paginator.get_page(page)

    # ================= CONTEXT =================
    return render(request, 'clients/list_client.html', {
        'clients': clients,
        'search_query': search_query,
        'statut_filter': statut_filter,

        'total_clients': total_clients,
        'actif_count': actif_count,
        'suspendu_count': suspendu_count,
        'resilie_count': resilie_count,
        'non_actif_count': non_actif_count,

        'actif_pourcentage': actif_pourcentage,
        'suspendu_pourcentage': suspendu_pourcentage,
        'resilie_pourcentage': resilie_pourcentage,
        'non_actif_pourcentage': non_actif_pourcentage,

        'is_commercial': is_commercial,
    })



@login_required
@is_allowed_roles(['admin', 'superviseur','commercial'])
#fonction pour afficher le formulaire detail.
def detail_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'clients/detail_client.html', {'client': client})



@login_required
@is_allowed_roles(['admin', 'superviseur'])
#Fonction pour la modification d'un client
def modifier_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':

        def clean_value(value):
            value = value.strip() if value else ''
            return value if value else None

        # ================= CLIENT =================
        client.nom_client = request.POST.get('nom_client', client.nom_client)
        client.adresse = request.POST.get('adresse', client.adresse)
        client.quartier = clean_value(request.POST.get('quartier'))
        client.telephone = clean_value(request.POST.get('telephone'))
        client.email = clean_value(request.POST.get('email'))
        client.statut = request.POST.get('statut', client.statut)

        # ================= TECHNIQUE =================
        client.vlan = clean_value(request.POST.get('vlan'))
        client.capacite = clean_value(request.POST.get('capacite'))
        client.download = clean_value(request.POST.get('download'))
        client.upload = clean_value(request.POST.get('upload'))
        client.forfait = clean_value(request.POST.get('forfait'))  
        client.adresse_ip = clean_value(request.POST.get('adresse_ip'))

        if client.adresse_ip:
            try:
                validate_ipv46_address(client.adresse_ip)
            except ValidationError:
                messages.error(request, "❌ Adresse IP invalide")
                return redirect('clients:modifier_client', client.id)

        # ================= COMMERCIAL =================
        commercial_id = request.POST.get('commercial_id')
        if commercial_id and commercial_id.isdigit():
            client.commercial = Commercial.objects.filter(id=commercial_id).first()
        else:
            client.commercial = None

        # ================= TYPE CONTRAT =================
        type_contrat_id = request.POST.get('type_contrat')
        if type_contrat_id and type_contrat_id.isdigit():
            client.type_contrat = TypeContrat.objects.filter(id=type_contrat_id).first()
        else:
            client.type_contrat = None

        # ================= BASE STATION =================
        base_station_id = request.POST.get('base_station')
        if base_station_id and base_station_id.isdigit():
            client.base_station = BaseStation.objects.filter(id=base_station_id).first()
        else:
            client.base_station = None

        # ================= PDF =================
        if 'contrat_pdf' in request.FILES:
            if client.contrat_pdf:
                client.contrat_pdf.delete(save=False)
            client.contrat_pdf = request.FILES['contrat_pdf']

        client.save()

        messages.success(request, f'✅ Client "{client.nom_client}" modifié avec succès!')
        return redirect('clients:list_client')

    # ================= DATA POUR FORM =================
<<<<<<< HEAD
    commerciaux = Commercial.objects.all().order_by('employe__nom', 'employe__prenom')
=======
    commerciaux = Commercial.objects.all().order_by('nom', 'prenom')
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
    base_stations = BaseStation.objects.all().order_by('nom')
    types_contrat = TypeContrat.objects.all().order_by('nom')

    context = {
        'client': client,
        'commerciaux': commerciaux,
        'base_stations': base_stations,
        'types_contrat': types_contrat,
    }

    return render(request, 'clients/modifier_client.html', context)



@login_required
@is_allowed_roles(['admin', 'superviseur'])
#Fonction pour la suppression d'un client
@login_required
def supprimer_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    client_name = client.nom_client
    
    # Vérifier si l'utilisateur a le droit de supprimer ce client
    user = request.user
<<<<<<< HEAD
    commercial = Commercial.objects.filter(employe__user_account=user).first()
=======
    commercial = Commercial.objects.filter(user_account=user).first()
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
    
    # Si c'est un commercial, vérifier que le client lui appartient
    if commercial and client.commercial != commercial:
        messages.error(request, "Vous n'avez pas le droit de supprimer ce client.")
        return redirect('clients:list_client')
    
    # 🔥 SOFT DELETE : Marquer comme supprimé sans effacer les données
    client.est_supprime = True
    client.date_suppression = timezone.now()
    client.statut = 'resilie'  # Changer le statut en résilié
    client.save()
    
    # Message de confirmation
    messages.warning(
        request, 
        f'⚠️ Le client "{client_name}" a été désactivé/supprimé.\n'
        f'Ses activités et son contrat sont conservés dans l\'historique.'
    )
    
    return redirect('clients:list_client')

@login_required
@is_allowed_roles(['admin', 'superviseur','commercial'])
#Fonction pour afficher le pdf
def voir_pdf(request, client_id):
        """Afficher le PDF d'un client"""
        client = get_object_or_404(Client, id=client_id)

        if client.contrat_pdf:
            # Ouvrir le fichier PDF
            pdf_file = open(client.contrat_pdf.path, 'rb')

            # Retourner le PDF comme réponse
            response = FileResponse(pdf_file, content_type='application/pdf')

            # Optionnel: afficher dans le navigateur plutôt que télécharger
            response['Content-Disposition'] = f'inline; filename="{client.contrat_pdf.name}"'

            return response
        else:
            messages.error(request, "Aucun fichier PDF disponible")
            return redirect('detail_client', client_id=client_id)


@login_required
@is_allowed_roles(['admin', 'superviseur']) 
#@user_passes_test(is_commercial)
#Le module des cativités
def ajouter_activite_avec_client(request, client_id):

    client = get_object_or_404(Client, id=client_id)
<<<<<<< HEAD
    techniciens = Technicien.objects.all().order_by('employe__nom', 'employe__prenom')
=======
    techniciens = Technicien.objects.all().order_by('nom', 'prenom')
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad

    if request.method == "POST":

        # ================= INFOS PRINCIPALES =================
        type_activite = request.POST.get("type_activite")
        date_activite = request.POST.get("date_activite")
        lieu = request.POST.get("lieu")
        description = request.POST.get("description")
        statut = request.POST.get("statut")
        heure_debut = request.POST.get("heure_debut") or None
        heure_fin = request.POST.get("heure_fin") or None

        technicien_ids = request.POST.getlist("techniciens")

        # ================= VALIDATION =================
        if not type_activite or not date_activite or not statut:
            messages.error(request, "❌ Veuillez remplir les champs obligatoires")
            return redirect('clients:ajouter_activite_avec_client', client_id=client_id)

        # ================= CREATION ACTIVITE =================
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

        # ================= TECHNICIENS =================
        if technicien_ids:
            activite.techniciens.set(technicien_ids)

        # ================= 🔥 GESTION PROSPECTION =================
        if type_activite == "prospection":

            zone = request.POST.get("zone")
            potentiel = request.POST.get("potentiel")
            observation = request.POST.get("observation")

            # 👉 OPTION SIMPLE (rapide)
            activite.description += f"""

            --- PROSPECTION ---
            Zone: {zone}
            Potentiel: {potentiel}
            Observation: {observation}
            """

            activite.save()

            # 👉 OPTION PRO (commentée pour plus tard)
            # Prospection.objects.create(
            #     activite=activite,
            #     zone=zone,
            #     potentiel=potentiel,
            #     observation=observation
            # )

        # ================= SUCCESS =================
        messages.success(request, "✅ Activité ajoutée avec succès")

        return redirect('clients:detail_client', client_id=client_id)

    # ================= GET =================
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
@is_allowed_roles(['admin', 'superviseur']) 
#@user_passes_test(is_commercial)
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
<<<<<<< HEAD
            client = Client.objects.filter(id=client_id, est_supprime=False).get()
=======
            client = Client.objects.get(id=client_id)
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad

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

            return redirect('clients:detail_client', client_id)

        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')

<<<<<<< HEAD
    clients = Client.objects.filter(est_supprime=False).order_by('nom_client')
    techniciens = Technicien.objects.all().order_by('employe__nom', 'employe__prenom')
=======
    clients = Client.objects.all().order_by('nom_client')
    techniciens = Technicien.objects.all().order_by('nom', 'prenom')
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad

    return render(request, 'clients/ajouter_activite.html',{
        'clients': clients,
        'techniciens': techniciens,
        'types_activite': Activite.TYPE_ACTIVITE_CHOICES,
        'statuts': Activite.STATUT_CHOICES,
        'aujourdhui': date.today().isoformat(),
    })

@login_required
@is_allowed_roles(['admin', 'superviseur','commercial'])  
#@user_passes_test(is_commercial)
def list_activite(request):
    # 🔐 Si technicien → il ne voit que ses activités
    if request.user.user_type.lower() == "technicien":

<<<<<<< HEAD
        # ✅ CORRECTED: Access technicien_profile through employe relationship
        # Original code (commented): if not hasattr(request.user, "technicien"):
        # Original code (commented):     return redirect("dashboard")
        # Original code (commented): technicien = request.user.technicien
        
        if not (request.user.employe and hasattr(request.user.employe, 'technicien_profile') and request.user.employe.technicien_profile):
            return redirect("dashboard")

        technicien = request.user.employe.technicien_profile

        activites_list = Activite.objects.filter(
            techniciens=technicien
        ).select_related('rapport', 'client')

    else:
        # Admin / Superviseur / Commercial
        activites_list = Activite.objects.all().select_related('rapport', 'client')
=======
        if not hasattr(request.user, "technicien"):
            return redirect("dashboard")

        technicien = request.user.technicien

        activites_list = Activite.objects.filter(
            techniciens=technicien
        )

    else:
        # Admin / Superviseur / Commercial
        activites_list = Activite.objects.all()
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad


    """Liste toutes les activités"""
    search_query = request.GET.get('search', '')
    statut_filter = request.GET.get('statut', '')
    type_filter = request.GET.get('type', '')
    date_filter = request.GET.get('date', '')



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
    paginator = Paginator(activites_list, 10)
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
@is_allowed_roles(['admin', 'superviseur','commercial'])
#@user_passes_test(is_commercial)
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
@is_allowed_roles(['admin', 'superviseur','commercial'])
#@user_passes_test(is_commercial)
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
@is_allowed_roles(['admin', 'superviseur','commercial','technicien']) 
#@user_passes_test(is_commercial)
def detail_activite(request, pk):
    activite = get_object_or_404(Activite, pk=pk)

    context = {
        'activite': activite
    }

    return render(request, 'clients/detail_activite.html', context)

@login_required
@is_allowed_roles(['admin', 'superviseur'])
#@user_passes_test(is_commercial)
def modifier_activite(request, pk):
    """Modifier une activité"""
    activite = get_object_or_404(
        Activite.objects.prefetch_related('techniciens'),
        pk=pk
    )

<<<<<<< HEAD
    # 🔒 INTERDIRE LA MODIFICATION D'ACTIVITÉS TERMINÉES
    if activite.statut == 'termine':
        messages.error(request, "❌ Impossible de modifier une activité terminée.")
        return redirect('clients:detail_activite', pk=activite.pk)

=======
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
    if request.method == 'POST':

        client_id = request.POST.get('client_id')
        type_activite = request.POST.get('type_activite')
        date_activite = request.POST.get('date_activite')
        heure_debut = request.POST.get('heure_debut')
        heure_fin = request.POST.get('heure_fin')
        description = request.POST.get('description', '').strip()
        lieu = request.POST.get('lieu', '').strip()
        statut = request.POST.get('statut')

        # IMPORTANT pour ManyToMany
        techniciens_ids = request.POST.getlist('techniciens')
        if hasattr(request.user, 'technicien'):
            #raise PermissionDenied
            pass

        # Validation
        if not client_id or not type_activite or not date_activite:
            messages.error(request, 'Tous les champs obligatoires doivent être remplis')
            return redirect('clients:modifier_activite', pk=activite.pk)

        try:
<<<<<<< HEAD
            activite.client = Client.objects.filter(id=client_id, est_supprime=False).get()
=======
            activite.client = Client.objects.get(id=client_id)
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
            activite.type_activite = type_activite
            activite.date_activite = date_activite
            activite.heure_debut = heure_debut or None
            activite.heure_fin = heure_fin or None
            activite.description = description or None
            activite.lieu = lieu or None
            activite.statut = statut

            activite.save()

            # 🔥 Mise à jour ManyToMany
            activite.techniciens.set(techniciens_ids)

            messages.success(request, 'Activité modifiée avec succès!')
            return redirect('clients:detail_activite', pk=activite.pk)

        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')

    # GET
<<<<<<< HEAD
    clients = Client.objects.filter(est_supprime=False).order_by('nom_client')
    techniciens = Technicien.objects.all().order_by('employe__nom', 'employe__prenom')
=======
    clients = Client.objects.all().order_by('nom_client')
    techniciens = Technicien.objects.all().order_by('nom', 'prenom')
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad

    context = {
        'activite': activite,
        'clients': clients,
        'techniciens': techniciens,
        'types_activite': Activite.TYPE_ACTIVITE_CHOICES,
        'statuts': Activite.STATUT_CHOICES,
    }

    return render(request, 'clients/modifier_activite.html', context)

@login_required
@is_allowed_roles(['admin', 'superviseur'])
#@user_passes_test(is_commercial)
@login_required
def supprimer_activite(request, pk):
    activite = get_object_or_404(Activite, pk=pk)

    if request.user.user_type == "technicien":
        messages.error(request, "❌ Action non autorisée")
        return redirect('clients:list_activite')

    if request.method == 'POST':
        client_nom = activite.client.nom_client
        activite.delete()

        messages.success(request, f'✅ Activité pour {client_nom} supprimée avec succès!')
        return redirect('clients:list_activite')

    return redirect('clients:list_activite')

#la liste des activités par client


@login_required
@is_allowed_roles(['admin', 'superviseur'])
#@user_passes_test(is_commercial)
def liste_activites_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    activites = Activite.objects.filter(client=client).order_by('-date_activite')

    context = {
        'client': client,
        'activites': activites,
    }

    return render(request, 'clients/liste_activites_client.html', context)

@login_required
#@user_passes_test(is_commercial)
@is_allowed_roles(['admin', 'superviseur','commercial','technicien'])
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


#La vue des mes activités pour les techniciens connectés


@login_required
@is_allowed_roles(['admin', 'technicien'])
def mes_activites(request):

    user = request.user

    # 🔒 sécurité supplémentaire (au cas où le décorateur change)
    if user.user_type not in ['admin', 'technicien']:
        return HttpResponseForbidden("Accès refusé")

    # =========================
    # 🔧 TECHNICIEN
    # =========================
    if user.user_type == "technicien":

<<<<<<< HEAD
        # ✅ CORRECTED: Access technicien_profile through employe relationship
        # Original code (commented): technicien = getattr(user, 'technicien', None)
        
        technicien = None
        if user.employe and hasattr(user.employe, 'technicien_profile'):
            technicien = user.employe.technicien_profile
=======
        technicien = getattr(user, 'technicien', None)
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad

        if not technicien:
            return HttpResponseForbidden(
                "Aucun profil technicien associé à votre compte"
            )

        activites = Activite.objects.filter(
            techniciens=technicien
        ).order_by('-date_activite')

    # =========================
    # 👑 ADMIN
    # =========================
    else:  # admin

        activites = Activite.objects.all().order_by('-date_activite')

    return render(request, 'clients/mes_activites.html', {
        'activites': activites
    })
    
    
@login_required    
@is_allowed_roles(['technicien'])
def modifier_rapport(request, rapport_id):

    rapport = get_object_or_404(RapportActivite, id=rapport_id)
    activite = rapport.activite

<<<<<<< HEAD
    # 🔒 sécurité : seul le technicien qui a créé le rapport peut modifier
    technicien = Technicien.objects.filter(employe__user_account=request.user).first()
    if not technicien:
        messages.error(request, "❌ Aucun profil technicien associé à votre compte.")
        return redirect('clients:mes_activites')

    # 🔒 VÉRIFIER QUE LE TECHNICIEN A CRÉÉ CE RAPPORT
    if rapport.technicien != technicien:
        messages.error(request, "❌ Vous n'êtes pas l'auteur de ce rapport. Vous ne pouvez pas le modifier.")
        return redirect('clients:mes_activites')
=======
    # 🔒 sécurité : seul le technicien peut modifier
    technicien = Technicien.objects.filter(user=request.user).first()
    if not technicien:
        return redirect('rapportActivites:liste_activites_technicien')

    if rapport.technicien != technicien:
        return redirect('rapportActivites:liste_activites_technicien')
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad

    if request.method == "POST":

        form = RapportActiviteForm(
            request.POST,
            request.FILES,
            instance=rapport,
            activite=activite
        )

        if form.is_valid():
            form.save()

            return redirect('rapportActivites:liste_activites_technicien')

    else:
        form = RapportActiviteForm(
            instance=rapport,
            activite=activite
        )

    return render(request, "rapportsActivites/creer_rapport.html", {
        "form": form,
        "activite": activite
    })
    

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
    


   