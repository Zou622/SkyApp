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
<<<<<<< HEAD
from employes.models import Employe
=======
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad


 #fonction pour afficher le formulaire de liste commercial.

# Liste des commerciaux
@login_required
def list_commercial(request):
    search_query = request.GET.get('search', '')

    if search_query:
        commerciaux_list = Commercial.objects.filter(
<<<<<<< HEAD
            Q(employe__nom__icontains=search_query) |
            Q(employe__prenom__icontains=search_query) |
            Q(employe__telephone__icontains=search_query) |
            Q(employe__email__icontains=search_query) |
            Q(employe__quartier__icontains=search_query)
        ).order_by('employe__nom', 'employe__prenom')
    else:
        commerciaux_list = Commercial.objects.all().order_by('employe__nom', 'employe__prenom')
=======
            Q(nom__icontains=search_query) |
            Q(prenom__icontains=search_query) |
            Q(telephone__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(quartier__icontains=search_query)
        ).order_by('nom', 'prenom')
    else:
        commerciaux_list = Commercial.objects.all().order_by('nom', 'prenom')
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad

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
<<<<<<< HEAD
    eligible_employes = Employe.objects.filter(commercial_profile__isnull=True).order_by('nom', 'prenom')

    if request.method == 'POST':
        employe_id = request.POST.get('employe_id')
        taux_commission = request.POST.get('taux_commission')
        statut = request.POST.get('statut', 'actif')
        est_actif = statut == 'actif'

        if not employe_id:
            messages.error(request, 'Veuillez sélectionner un employé pour créer le commercial.')
            return render(request, 'commercials/ajouter_commercial.html', {
                'eligible_employes': eligible_employes,
            })

        employe = get_object_or_404(Employe, id=employe_id)
        if hasattr(employe, 'commercial_profile') and employe.commercial_profile is not None:
            messages.error(request, 'Cet employé est déjà rattaché à un commercial.')
            return render(request, 'commercials/ajouter_commercial.html', {
                'eligible_employes': eligible_employes,
            })

        try:
            Commercial.objects.create(
                employe=employe,
                taux_commission=taux_commission if taux_commission else 10.00,
                est_actif=est_actif
            )
            # Mettre à jour la fonction de l'employé
            employe.fonction = 'commercial'
            employe.save(update_fields=['fonction'])
            messages.success(request, f'Commercial {employe.nom} {employe.prenom} ajouté avec succès!')
=======
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

        # Créer le commercial
        try:
            commercial = Commercial.objects.create(
                nom=nom,
                prenom=prenom,
                telephone=telephone,
                email=email if email else None,
                quartier=quartier if quartier else None,
                adresse=adresse if adresse else None,
                specialite=specialite if specialite else 'vente',
                taux_commission=taux_commission if taux_commission else 10.00,
                date_embauche=date_embauche if date_embauche else None,
                est_actif=est_actif
            )

            messages.success(request, f'Commercial {nom} {prenom} ajouté avec succès!')
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
            return redirect('list_commercial')

        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
<<<<<<< HEAD

    # GET request - afficher le formulaire vide
    return render(request, 'commercials/ajouter_commercial.html', {
        'eligible_employes': eligible_employes,
    })
=======
            return render(request, 'commercials/ajouter_commercial.html')

    # GET request - afficher le formulaire vide
    SPECIALITES = Commercial.SPECIALITES
    context = {'specialites': SPECIALITES}
    return render(request, 'commercials/ajouter_commercial.html', context)
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad




# Modifier un commercial
@login_required
def modifier_commercial(request, pk):
    commercial = get_object_or_404(Commercial, pk=pk)

    if request.method == 'POST':
        # Récupérer les données du formulaire
<<<<<<< HEAD
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        quartier = request.POST.get('quartier')
        adresse = request.POST.get('adresse')
        taux_commission = request.POST.get('taux_commission')
        date_embauche = request.POST.get('date_embauche')
        statut = request.POST.get('statut', 'actif')
        est_actif = statut == 'actif'

        # Validation
        if not nom or not prenom:
            messages.error(request, 'Nom et Prénom sont obligatoires')
            context = {
                'commercial': commercial,
=======
        commercial.nom = request.POST.get('nom')
        commercial.prenom = request.POST.get('prenom')
        commercial.telephone = request.POST.get('telephone')
        commercial.email = request.POST.get('email')
        commercial.quartier = request.POST.get('quartier')
        commercial.adresse = request.POST.get('adresse')
        commercial.specialite = request.POST.get('specialite')
        commercial.taux_commission = request.POST.get('taux_commission')
        #commercial.date_embauche = request.POST.get('date_embauche')
        commercial.est_actif = request.POST.get('est_actif') == 'on'
        
        #même si la date d'embauche est facultative, on doit vérifier si elle est fournie avant de l'assigner
        date_embauche = request.POST.get('date_embauche')
        if date_embauche:
            commercial.date_embauche = date_embauche
        else:
            commercial.date_embauche = None


        # Validation
        if not commercial.nom or not commercial.prenom:
            messages.error(request, 'Nom et Prénom sont obligatoires')
            context = {
                'commercial': commercial,
                'specialites': Commercial.SPECIALITES
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
            }
            return render(request, 'commercials/modifier_commercial.html', context)

        try:
<<<<<<< HEAD
            # Modifier l'employé lié
            commercial.employe.nom = nom
            commercial.employe.prenom = prenom
            commercial.employe.telephone = telephone or commercial.employe.telephone
            if email is not None:
                commercial.employe.email = email or ''
            if quartier is not None:
                commercial.employe.quartier = quartier or None
            if adresse is not None:
                commercial.employe.adresse = adresse or ''
            if date_embauche:
                commercial.employe.date_embauche = date_embauche
            commercial.employe.save()

            # Modifier le commercial
            commercial.taux_commission = taux_commission if taux_commission else 10.00
            commercial.est_actif = est_actif
            commercial.save()

            messages.success(request, f'Commercial {nom} {prenom} modifié avec succès!')
=======
            commercial.save()
            messages.success(request, f'Commercial {commercial.nom} {commercial.prenom} modifié avec succès!')
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
            return redirect('detail_commercial', pk=commercial.pk)

        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            context = {
                'commercial': commercial,
<<<<<<< HEAD
=======
                'specialites': Commercial.SPECIALITES
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
            }
            return render(request, 'commercials/modifier_commercial.html', context)

    # GET request - afficher le formulaire avec les données
    context = {
        'commercial': commercial,
<<<<<<< HEAD
=======
        'specialites': Commercial.SPECIALITES
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
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
<<<<<<< HEAD
        nom_complet = f"{commercial.employe.nom} {commercial.employe.prenom}"
        # Remettre la fonction de l'employé à None
        commercial.employe.fonction = None
        commercial.employe.save(update_fields=['fonction'])
        commercial.delete()
        messages.success(request, f'Commercial {nom_complet} supprimé avec succès!')
=======
        #nom_complet = commercial.nom_complet()
        commercial.delete()
        messages.success(request, f'Commercial {commercial.nom}  {commercial.prenom}  supprimé avec succès!')
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
        return redirect('list_commercial')

    context = {'commercial': commercial}
    return render(request, 'commercials/supprimer_commercial.html', context)