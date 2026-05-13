from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Technicien
from employes.models import Employe
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
            Q(employe__nom__icontains=search_query) |
            Q(employe__prenom__icontains=search_query) |
            Q(employe__email__icontains=search_query) |
            Q(employe__telephone__icontains=search_query) |
            Q(employe__quartier__icontains=search_query)
        )

    techniciens_list = techniciens_list.order_by('employe__nom', 'employe__prenom')

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
    employes = Employe.objects.filter(technicien_profile__isnull=True).order_by('nom', 'prenom')
    return render(request, 'techniciens/ajouter_technicien.html', {
        'employes': employes,
    })


@login_required
def enregistrer_technicien(request):
    """Enregistrer un nouveau technicien"""
    if request.method == 'POST':
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

        messages.success(request, f'✅ Technicien "{employe.nom} {employe.prenom}" ajouté avec succès!')
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


@login_required
def supprimer_technicien(request, technicien_id):
    """Supprimer un technicien"""
    technicien = get_object_or_404(Technicien, id=technicien_id)

    if request.method == 'POST':
        nom_complet = f"{technicien.employe.nom} {technicien.employe.prenom}"
        technicien.delete()
        messages.success(request, f'❌ Technicien "{nom_complet}" supprimé avec succès!')
        return redirect('list_technicien')

    return render(request, 'techniciens/supprimer_technicien.html', {'technicien': technicien})