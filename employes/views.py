from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Employe, Poste
from .forms import EmployeForm, PosteForm
from users.decorators import user_type_required

User = get_user_model()


@login_required
@user_type_required(['admin', 'rh'])
def liste_employes(request):

    #  RECHERCHE
    search = request.GET.get("search")

    employes = Employe.objects.all().order_by("-id")

    if search:
        employes = employes.filter(
            Q(nom__icontains=search)
            | Q(prenom__icontains=search)
            | Q(matricule__icontains=search)
            | Q(telephone__icontains=search)
        )

    #  PAGINATION
    paginator = Paginator(employes, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    #  STATISTIQUES
    total_employes = employes.count()
    active_employes = employes.filter(statut='Actif').count()

    context = {
        "page_obj": page_obj,
        "search": search,
        "total_employes": total_employes,
        "active_employes": active_employes,
    }

    return render(request, "employes/liste_employes.html", context)


@login_required
@user_type_required(['admin', 'rh'])
def ajouter_employe(request):

    if request.method == "POST":

        form = EmployeForm(request.POST, request.FILES)

        if form.is_valid():

            employe = form.save()

            messages.success(
                request,
                f"L'employé {employe.nom} {employe.prenom} a été ajouté avec succès.",
            )

            return redirect("employes:liste_employes")

        else:

            messages.error(request, "Veuillez corriger les erreurs du formulaire.")

    else:

        form = EmployeForm()

    context = {"form": form, "titre": "Ajouter un employé"}

    return render(request, "employes/ajout_employes.html", context)


@login_required
@user_type_required(['admin', 'rh'])
def liste_postes(request):
    postes = Poste.objects.all().order_by('nom')
    return render(request, 'employes/liste_postes.html', {
        'postes': postes,
    })


@login_required
@user_type_required(['admin', 'rh'])
def ajouter_poste(request):
    form = PosteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        poste = form.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'id': poste.id, 'nom': poste.nom})
        messages.success(request, 'Poste ajouté avec succès.')
        return redirect('employes:liste_postes')

    return render(request, 'employes/ajout_poste.html', {
        'form': form,
        'titre': 'Ajouter un poste',
    })


@login_required
@user_type_required(['admin', 'rh'])
def supprimer_poste(request, poste_id):
    poste = get_object_or_404(Poste, id=poste_id)
    if request.method == 'POST':
        poste.delete()
        messages.success(request, 'Poste supprimé avec succès.')
        return redirect('employes:liste_postes')
    return render(request, 'employes/confirmer_suppression.html', {
        'objet': poste,
        'type': 'poste',
        'retour_url': 'employes:liste_postes',
    })


@login_required
@user_type_required(['admin', 'rh'])
def detail_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)
    context = {
        'employe': employe,
    }
    return render(request, 'employes/detail_employes.html', context)


@login_required
@user_type_required(['admin', 'rh'])
def modifier_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)
    
    if request.method == 'POST':
        form = EmployeForm(request.POST, request.FILES, instance=employe)
        if form.is_valid():
            employe = form.save()
            messages.success(request, f"L'employé {employe.nom} {employe.prenom} a été modifié avec succès.")
            return redirect('employes:detail_employe', employe_id=employe.id)
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = EmployeForm(instance=employe)
    
    context = {
        'form': form,
        'titre': 'Modifier un employé',
        'employe': employe,
    }
    return render(request, 'employes/modifier_employes.html', context)


@login_required
@user_type_required(['admin', 'rh'])
def supprimer_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)
    if request.method == 'POST':
        # Supprimer la fiche commerciale/technicien liée pour éviter les enregistrements orphelins
        if hasattr(employe, 'commercial_profile') and employe.commercial_profile is not None:
            employe.commercial_profile.delete()
        if hasattr(employe, 'technicien_profile') and employe.technicien_profile is not None:
            employe.technicien_profile.delete()

        employe.delete()
        messages.success(request, f"L'employé {employe.nom} {employe.prenom} a été supprimé avec succès.")
        return redirect('employes:liste_employes')
    return render(request, 'employes/confirmer_suppression.html', {
        'objet': employe,
        'type': 'employé',
        'retour_url': 'employes:liste_employes',
    })


@login_required
@user_type_required(['admin', 'rh'])
def creer_compte_utilisateur(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)

    fonction_role_map = {
        'commercial': 'commercial',
        'technicien': 'technicien',
    }

    if employe.has_user_account:
        messages.warning(request, "Cet employé a déjà un compte utilisateur.")
        return redirect('employes:liste_employes')

    auto_user_type = fonction_role_map.get(employe.fonction)

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        user_type = auto_user_type or request.POST.get('user_type')

        if not username or not password or not confirm_password or not user_type:
            messages.error(request, "Tous les champs obligatoires doivent être remplis.")
        elif password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà.")
        else:
            user = User.objects.create_user(
                username=username,
                first_name=employe.prenom,
                last_name=employe.nom,
                email=employe.email or '',
                user_type=user_type,
                password=password,
                employe=employe
            )
            messages.success(request, f"Compte utilisateur créé pour {employe.nom} {employe.prenom}.")
            return redirect('employes:liste_employes')

    context = {
        'employe': employe,
        'user_types': User.TYPE_USER,
        'auto_user_type': auto_user_type,
    }
    return render(request, "employes/creer_compte.html", context)
