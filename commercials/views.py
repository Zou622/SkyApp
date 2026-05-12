from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Commercial
from datetime import date
from django.contrib.auth.decorators import login_required


 #fonction pour afficher le formulaire de liste commercial.

# Liste des commerciaux
@login_required
def list_commercial(request):
    search_query = request.GET.get('search', '')

    if search_query:
        commerciaux_list = Commercial.objects.filter(
            Q(employe__nom__icontains=search_query) |
            Q(employe__prenom__icontains=search_query) |
            Q(employe__telephone__icontains=search_query) |
            Q(employe__email__icontains=search_query) |
            Q(employe__quartier__icontains=search_query)
        ).order_by('employe__nom', 'employe__prenom')
    else:
        commerciaux_list = Commercial.objects.all().order_by('employe__nom', 'employe__prenom')

    paginator = Paginator(commerciaux_list, 10)
    page_number = request.GET.get('page')
    commerciaux = paginator.get_page(page_number)

    context = {
        'commerciaux': commerciaux,
        'search_query': search_query,
        'total_commerciaux': Commercial.objects.count(),
        'commerciaux_actifs': Commercial.objects.filter(est_actif=True).count(),
    }
    return render(request, 'commercials/list_commercial.html', context)


# Ajouter un commercial
@login_required
def ajouter_commercial(request):
    from employes.models import Employe
    from django.utils import timezone

    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        quartier = request.POST.get('quartier')
        adresse = request.POST.get('adresse')
        specialite = request.POST.get('specialite')
        taux_commission = request.POST.get('taux_commission')
        date_embauche = request.POST.get('date_embauche')
        est_actif = request.POST.get('est_actif') == 'on'

        # Validation simple
        if not nom or not prenom:
            messages.error(request, 'Nom et Prénom sont obligatoires')
            return render(request, 'commercials/ajouter_commercial.html')

        try:
            # Créer d'abord l'employé
            employe = Employe.objects.create(
                nom=nom,
                prenom=prenom,
                telephone=telephone,
                email=email if email else None,
                quartier=quartier if quartier else None,
                adresse=adresse if adresse else None,
                date_embauche=date_embauche if date_embauche else date.today(),
                statut='Actif'
            )

            # Créer le commercial lié à l'employé
            commercial = Commercial.objects.create(
                employe=employe,
                specialite=specialite if specialite else 'vente',
                taux_commission=taux_commission if taux_commission else 10.00,
                est_actif=est_actif
            )

            messages.success(request, f'Commercial {nom} {prenom} ajouté avec succès!')
            return redirect('list_commercial')

        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return render(request, 'commercials/ajouter_commercial.html')

    # GET request - afficher le formulaire vide
    SPECIALITES = Commercial.SPECIALITES
    context = {'specialites': SPECIALITES}
    return render(request, 'commercials/ajouter_commercial.html', context)




# Modifier un commercial
@login_required
def modifier_commercial(request, pk):
    commercial = get_object_or_404(Commercial, pk=pk)

    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        quartier = request.POST.get('quartier')
        adresse = request.POST.get('adresse')
        specialite = request.POST.get('specialite')
        taux_commission = request.POST.get('taux_commission')
        date_embauche = request.POST.get('date_embauche')
        est_actif = request.POST.get('est_actif') == 'on'

        # Validation
        if not nom or not prenom:
            messages.error(request, 'Nom et Prénom sont obligatoires')
            context = {
                'commercial': commercial,
                'specialites': Commercial.SPECIALITES
            }
            return render(request, 'commercials/modifier_commercial.html', context)

        try:
            # Modifier l'employé lié
            commercial.employe.nom = nom
            commercial.employe.prenom = prenom
            commercial.employe.telephone = telephone
            commercial.employe.email = email if email else None
            commercial.employe.quartier = quartier if quartier else None
            commercial.employe.adresse = adresse if adresse else None
            if date_embauche:
                commercial.employe.date_embauche = date_embauche
            commercial.employe.save()

            # Modifier le commercial
            commercial.specialite = specialite if specialite else 'vente'
            commercial.taux_commission = taux_commission if taux_commission else 10.00
            commercial.est_actif = est_actif
            commercial.save()

            messages.success(request, f'Commercial {nom} {prenom} modifié avec succès!')
            return redirect('detail_commercial', pk=commercial.pk)

        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            context = {
                'commercial': commercial,
                'specialites': Commercial.SPECIALITES
            }
            return render(request, 'commercials/modifier_commercial.html', context)

    # GET request - afficher le formulaire avec les données
    context = {
        'commercial': commercial,
        'specialites': Commercial.SPECIALITES
    }
    return render(request, 'commercials/modifier_commercial.html', context)


# Détails d'un commercial
@login_required
def detail_commercial(request, pk):
    commercial = get_object_or_404(Commercial, pk=pk)

    # Statistiques
    total_commission = 0  # À calculer selon vos besoins

    context = {
        'commercial': commercial,
        'total_commission': total_commission,
    }
    return render(request, 'commercials/detail_commercial.html', context)


# Supprimer un commercial
@login_required
def supprimer_commercial(request, pk):
    commercial = get_object_or_404(Commercial, pk=pk)

    if request.method == 'POST':
        nom_complet = f"{commercial.employe.nom} {commercial.employe.prenom}"
        commercial.delete()
        messages.success(request, f'Commercial {nom_complet} supprimé avec succès!')
        return redirect('list_commercial')

    context = {'commercial': commercial}
    return render(request, 'commercials/supprimer_commercial.html', context)