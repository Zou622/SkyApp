from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Technicien
<<<<<<< HEAD
from employes.models import Employe
=======
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
from django.contrib.auth.decorators import login_required, user_passes_test


# ========== VUES POUR LES TECHNICIENS ==========

@login_required
def list_technicien(request):
    """Liste des techniciens avec recherche"""
    search_query = request.GET.get('search', '').strip()
    statut_filter = request.GET.get('statut', '')

    # Filtrer les techniciens
    techniciens_list = Technicien.objects.all()

    if statut_filter:
        techniciens_list = techniciens_list.filter(statut=statut_filter)

    if search_query:
        techniciens_list = techniciens_list.filter(
<<<<<<< HEAD
            Q(employe__nom__icontains=search_query) |
            Q(employe__prenom__icontains=search_query) |
            Q(employe__email__icontains=search_query) |
            Q(employe__telephone__icontains=search_query) |
            Q(employe__quartier__icontains=search_query)
        )

    techniciens_list = techniciens_list.order_by('employe__nom', 'employe__prenom')
=======
            Q(nom__icontains=search_query) |
            Q(prenom__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(telephone__icontains=search_query) |
            Q(quartier__icontains=search_query) |
            Q(specialite__icontains=search_query)
        )

    techniciens_list = techniciens_list.order_by('nom', 'prenom')
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad

    # Pagination
    page = request.GET.get('page', 1)
    paginate_by = 10

    paginator = Paginator(techniciens_list, paginate_by)

    try:
        techniciens = paginator.page(page)
    except PageNotAnInteger:
        techniciens = paginator.page(1)
    except EmptyPage:
        techniciens = paginator.page(paginator.num_pages)

    # Statistiques
    total_techniciens = Technicien.objects.count()
    actif_count = Technicien.objects.filter(statut='actif').count()
    inactif_count = Technicien.objects.filter(statut='inactif').count()
    conge_count = Technicien.objects.filter(statut='congé').count()
    mission_count = Technicien.objects.filter(statut='mission').count()

    context = {
        'techniciens': techniciens,
        'search_query': search_query,
        'statut_filter': statut_filter,
        'total_techniciens': total_techniciens,
        'actif_count': actif_count,
        'inactif_count': inactif_count,
        'conge_count': conge_count,
        'mission_count': mission_count,
    }

    return render(request, 'techniciens/list_technicien.html', context)


@login_required
def ajouter_technicien(request):
    """Afficher le formulaire d'ajout de technicien"""
<<<<<<< HEAD
    employes = Employe.objects.filter(technicien_profile__isnull=True).order_by('nom', 'prenom')
    return render(request, 'techniciens/ajouter_technicien.html', {
        'employes': employes,
    })
=======
    return render(request, 'techniciens/ajouter_technicien.html')
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad


@login_required
def enregistrer_technicien(request):
    """Enregistrer un nouveau technicien"""
    if request.method == 'POST':
<<<<<<< HEAD
        employe_id = request.POST.get('employe_id')
        statut = request.POST.get('statut', 'actif')
        est_actif = True

        if not employe_id:
            messages.error(request, 'Veuillez sélectionner un employé existant.')
            return redirect('ajouter_technicien')

        employe = get_object_or_404(Employe, id=employe_id)
        if hasattr(employe, 'technicien_profile') and employe.technicien_profile is not None:
            messages.error(request, 'Cet employé est déjà lié à un technicien.')
            return redirect('ajouter_technicien')

        technicien = Technicien(
            employe=employe,
            statut=statut,
            est_actif=est_actif,
        )
        technicien.save()
        
        # Mettre à jour la fonction de l'employé
        employe.fonction = 'technicien'
        employe.save(update_fields=['fonction'])

        messages.success(request, f'✅ Technicien "{employe.nom} {employe.prenom}" ajouté avec succès!')
=======
        # Récupérer les données
        nom = request.POST.get('nom', '').strip()
        prenom = request.POST.get('prenom', '').strip()
        email = request.POST.get('email', '').strip() or None
        telephone = request.POST.get('telephone', '').strip()
        quartier = request.POST.get('quartier', '').strip()
        adresse = request.POST.get('adresse', '').strip()
        specialite = request.POST.get('specialite', '').strip()
        statut = request.POST.get('statut', 'actif').strip()
        photo = request.FILES.get('photo')
        # pour gérer le cas où la date d'embauche n'est pas fournie
        date_embauche = request.POST.get('date_embauche') or None
        if date_embauche:
            date_embauche = date_embauche
        else:
            date_embauche = None

        # Validation
        if not nom or not prenom:
            messages.error(request, 'Le nom et le prénom sont obligatoires')
            return render(request, 'techniciens/ajouter_technicien.html')

        # Vérifier si l'email existe déjà
        if Technicien.objects.filter(email=email).exists():
            messages.error(request, f'Un technicien avec l\'email "{email}" existe déjà')
            return render(request, 'techniciens/ajouter_technicien.html')

        # Créer et sauvegarder le technicien
        technicien = Technicien(
            nom=nom,
            prenom=prenom,
            email=email,
            telephone=telephone,
            quartier=quartier,
            adresse=adresse,
            specialite=specialite,
            statut=statut,
            date_embauche=date_embauche,
            photo=photo
        )
        technicien.save()

        messages.success(request, f'✅ Technicien "{nom} {prenom}" ajouté avec succès!')
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
        return redirect('list_technicien')

    return redirect('ajouter_technicien')


@login_required
def detail_technicien(request, technicien_id):
    """Afficher les détails d'un technicien"""
    technicien = get_object_or_404(Technicien, id=technicien_id)
    return render(request, 'techniciens/detail_technicien.html', {'technicien': technicien})


@login_required
def modifier_technicien(request, technicien_id):
    """Modifier un technicien existant"""
    technicien = get_object_or_404(Technicien, id=technicien_id)
<<<<<<< HEAD
    employe = technicien.employe

    if request.method == 'POST':
        employe.nom = request.POST.get('nom', employe.nom)
        employe.prenom = request.POST.get('prenom', employe.prenom)
        email = request.POST.get('email')
        if email is not None:
            employe.email = email or ''
        employe.telephone = request.POST.get('telephone', employe.telephone)
        if 'quartier' in request.POST:
            employe.quartier = request.POST.get('quartier') or None
        if 'adresse' in request.POST:
            employe.adresse = request.POST.get('adresse') or ''
        date_embauche = request.POST.get('date_embauche', employe.date_embauche)
        employe.date_embauche = date_embauche or employe.date_embauche

        if 'photo' in request.FILES:
            employe.photo = request.FILES['photo']

        employe.save()

        technicien.statut = request.POST.get('statut', technicien.statut)
        if 'est_actif' in request.POST:
            technicien.est_actif = request.POST.get('est_actif') == 'on'
        technicien.save()

        messages.success(request, f'✅ Technicien "{employe.nom} {employe.prenom}" modifié avec succès!')
        return redirect('list_technicien')

    return render(request, 'techniciens/modifier_technicien.html', {
        'technicien': technicien,
    })
=======

    if request.method == 'POST':
        # Mettre à jour les données
        technicien.nom = request.POST.get('nom', technicien.nom)
        technicien.prenom = request.POST.get('prenom', technicien.prenom)
        technicien.email = request.POST.get('email', technicien.email) or None
        technicien.telephone = request.POST.get('telephone', technicien.telephone)
        technicien.quartier = request.POST.get('quartier', technicien.quartier)
        technicien.adresse = request.POST.get('adresse', technicien.adresse)
        technicien.specialite = request.POST.get('specialite', technicien.specialite)
        technicien.statut = request.POST.get('statut', technicien.statut)
        # pour gérer le cas où la date d'embauche n'est pas fournie
        technicien.date_embauche = request.POST.get('date_embauche', technicien.date_embauche) or None
        if technicien.date_embauche:
            technicien.date_embauche = technicien.date_embauche
        else:
            technicien.date_embauche = None

        # Gérer la photo (si une nouvelle photo est téléchargée)
        if 'photo' in request.FILES:
            technicien.photo = request.FILES['photo']

        technicien.save()
        messages.success(request, f'✅ Technicien "{technicien.nom} {technicien.prenom}" modifié avec succès!')
        return redirect('list_technicien')

    return render(request, 'techniciens/modifier_technicien.html', {'technicien': technicien})
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad


@login_required
def supprimer_technicien(request, technicien_id):
    """Supprimer un technicien"""
    technicien = get_object_or_404(Technicien, id=technicien_id)

    if request.method == 'POST':
<<<<<<< HEAD
        nom_complet = f"{technicien.employe.nom} {technicien.employe.prenom}"
        # Remettre la fonction de l'employé à None
        technicien.employe.fonction = None
        technicien.employe.save(update_fields=['fonction'])
=======
        nom_complet = f"{technicien.nom} {technicien.prenom}"
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
        technicien.delete()
        messages.success(request, f'❌ Technicien "{nom_complet}" supprimé avec succès!')
        return redirect('list_technicien')

    return render(request, 'techniciens/supprimer_technicien.html', {'technicien': technicien})