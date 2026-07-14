from django.conf import settings
from django.db import connection, models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q, Count

from commercials.models import Commercial
from .models import PasswordResetToken, User
from .forms import LoginForm, PasswordResetRequestForm, SetNewPasswordForm, UserProfileForm1, UserRegistrationForm, UserProfileForm
from .decorators import admin_required
from activites.models import Activite
from clients.models import Client
from django.contrib.auth.decorators import login_required
from users.models import User
from activites.models import Activite
from django.db.models import Count
from activites.models import Activite, Client
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import get_user_model
from activites.models import Activite
from clients.models import Client
from commercials.models import Commercial
from techniciens.models import Technicien

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import PasswordResetToken
from .forms import PasswordResetRequestForm, SetNewPasswordForm
from django.contrib.auth import get_user_model
from prospects.models import Prospect



def login_view(request):
    """Vue de connexion"""
    if request.user.is_authenticated:
        return redirect('users:dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.est_actif and user.est_valide:
                    login(request, user)
                    user.derniere_connexion = timezone.now()
                    user.save()

                    messages.success(request, f"✅ Bienvenue {user.get_full_name()}!")

                    # Redirection selon le type
                    if user.user_type == 'admin':
                        return redirect('users:dashboard')
                    elif user.user_type.lower() == 'technicien':
                        return redirect('clients:mes_activites')
                    elif user.user_type == 'commercial':
                        return redirect('clients:list_client')
                    else:
                        return redirect('users:dashboard')
                else:
                    messages.error(request, "⛔ Votre compte n'est pas actif ou validé")
        else:
            messages.error(request, "❌ Nom d'utilisateur ou mot de passe incorrect")
    else:
        form = LoginForm()

    return render(request, 'utilisateurs/login.html', {'form': form})

@login_required
def register_view(request):
    """Vue d'inscription"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.est_valide = False  # À valider par un admin
            user.save()

            messages.success(
                request,
                "✅ Inscription réussie ! Votre compte sera validé par un administrateur."
            )
            return redirect('users:login')
        else:
            messages.error(request, "❌ Erreur dans le formulaire")
    else:
        form = UserRegistrationForm()

    return render(request, 'utilisateurs/register.html', {'form': form})


@login_required
def logout_view(request):
    """Déconnexion"""
    logout(request)
    messages.info(request, "👋 À bientôt !")
    return redirect('users:login')



def is_manager(user):
    return user.is_authenticated and user.user_type in ['admin', 'superviseur']




 
@admin_required
def list_utilisateurs(request):
    """Liste tous les utilisateurs (admin seulement)"""
    users = User.objects.all().order_by('-date_inscription')

    # Filtres
    user_type = request.GET.get('type', '')
    est_valide = request.GET.get('valide', '')

    if user_type:
        users = users.filter(user_type=user_type)
    if est_valide:
        users = users.filter(est_valide=(est_valide == 'true'))

    return render(request, 'utilisateurs/list_utilisateurs.html', {
        'users': users,
        'user_type_actuel': user_type,
        'types_utilisateurs': User.TYPE_USER,
    })




@login_required
@require_POST
def valider_utilisateur(request, user_id):
    user = get_object_or_404(User, id=user_id)

    user.est_valide = True
    user.save()

    return JsonResponse({
        "success": True,
        "message": f"Utilisateur {user.username} validé avec succès"
    })


<<<<<<< HEAD
=======
@login_required
def soft_delete_utilisateur(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        user.est_actif = False  # désactive le compte
        user.save()
        return JsonResponse({"success": True, "message": "Utilisateur supprimé avec succès."})
    return JsonResponse({"success": False}, status=405)



>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
from django.contrib import messages

@login_required
def modifier_profile(request):
    user = request.user

    if request.method == "POST":
<<<<<<< HEAD
        form = UserProfileForm(request.POST, request.FILES, instance=user.employe, user=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profil modifié avec succès")
            return redirect('users:profile')

    else:
        form = UserProfileForm(instance=user.employe, user=user)
=======
        form = UserProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            user = form.save(commit=False)

            password = form.cleaned_data.get("password")

            if password:
                user.set_password(password)

            user.save()

            messages.success(request, "Profil modifié avec succès")

            return redirect('users:profile')

    else:
        form = UserProfileForm(instance=user)
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad

    return render(request, "utilisateurs/modifier_profile.html", {"form": form})



@login_required
def get_user_stats(user):
    """Statistiques selon le type d'utilisateur"""
    stats = {}

<<<<<<< HEAD
    # ✅ CORRECTED: Access technicien_profile through employe relationship
    # Original code (commented): if user.user_type == 'technicien' and user.technicien:
    
    if user.user_type == 'technicien' and user.employe and hasattr(user.employe, 'technicien_profile') and user.employe.technicien_profile:
        # Original code (commented): activites = Activite.objects.filter(techniciens=user.technicien)
        activites = Activite.objects.filter(techniciens=user.employe.technicien_profile)
=======
    if user.user_type == 'technicien' and user.technicien:
        activites = Activite.objects.filter(techniciens=user.technicien)
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
        stats['activites_total'] = activites.count()

        # ⚠️ IMPORTANT : Convertir la date en string
        aujourd_hui = timezone.now().date()
        stats['activites_aujourdhui'] = activites.filter(date_activite=aujourd_hui).count()
        # Le count() retourne un nombre, pas un objet date, donc c'est bon

        stats['en_cours'] = activites.filter(statut='en_cours').count()
        stats['planifie'] = activites.filter(statut='planifie').count()
        stats['termine'] = activites.filter(statut='termine').count()

<<<<<<< HEAD
    # ✅ CORRECTED: Access commercial_profile through employe relationship
    # Original code (commented): elif user.user_type == 'commercial' and user.commercial:
    
    elif user.user_type == 'commercial' and user.employe and hasattr(user.employe, 'commercial_profile') and user.employe.commercial_profile:
        from clients.models import Client
        # Original code (commented): stats['clients_total'] = Client.objects.filter(commercial=user.commercial).count()
        # Original code (commented): stats['clients_actifs'] = Client.objects.filter(commercial=user.commercial, statut='actif').count()
        
        stats['clients_total'] = Client.objects.filter(commercial=user.employe.commercial_profile).count()
        stats['clients_actifs'] = Client.objects.filter(commercial=user.employe.commercial_profile, statut='actif').count()
=======
    elif user.user_type == 'commercial' and user.commercial:
        from clients.models import Client
        stats['clients_total'] = Client.objects.filter(commercial=user.commercial).count()
        stats['clients_actifs'] = Client.objects.filter(commercial=user.commercial, statut='actif').count()
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad

    return stats

@login_required
def profile_view(request):
    return render(request, "utilisateurs/profile.html")


@login_required
def detail_user(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)

    context = {
        "user_obj": user_obj
    }

    return render(request, "utilisateurs/detail_user.html", context)



@login_required
def statistiques_techniciens(request):

    # Récupérer uniquement les utilisateurs techniciens
    techniciens = User.objects.filter(role='technicien')

    # Annoter avec le nombre d'activités
    techniciens_stats = techniciens.annotate(
        total_activites=Count('activite')
    )

    context = {
        'techniciens_stats': techniciens_stats
    }

    return render(request, 'utilisateurs/dashboard.html', context)


# 1️⃣ Demande de réinitialisation
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            token = PasswordResetToken.objects.create(user=user)
            reset_link = request.build_absolute_uri(
                reverse('users:password_reset_confirm', kwargs={'token': str(token.token)})
            )
            # Envoyer email
            send_mail(
                subject="Réinitialisation de votre mot de passe",
                message=f"Bonjour {user.username},\nCliquez sur ce lien pour réinitialiser votre mot de passe:\n{reset_link}\nCe lien est valide 1h.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
            return redirect('users:password_reset_done')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'utilisateurs/password_reset_request.html', {'form': form})


# 2️⃣ Confirmation que l'email a été envoyé
def password_reset_done(request):
    return render(request, 'utilisateurs/password_reset_done.html')


# 3️⃣ Formulaire nouveau mot de passe
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def password_reset_confirm(request, token):
    token_obj = get_object_or_404(PasswordResetToken, token=token)

    if request.method == "POST":
        if not token_obj.is_valid():
            return JsonResponse({'status': 'error', 'message': 'Le lien est invalide ou expiré.'})

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not password1 or not password2:
            return JsonResponse({'status': 'error', 'message': 'Remplissez tous les champs'})
        if password1 != password2:
            return JsonResponse({'status': 'error', 'message': 'Les mots de passe ne correspondent pas'})

        token_obj.user.set_password(password1)
        token_obj.user.save()
        token_obj.mark_used()
        return JsonResponse({'status': 'success', 'message': 'Mot de passe réinitialisé avec succès !'})

    return render(request, 'utilisateurs/password_reset_confirm.html', {'token': token})


def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Cet email n’existe pas.'})

        token = PasswordResetToken.objects.create(user=user)
        reset_link = request.build_absolute_uri(
            reverse('users:password_reset_confirm', kwargs={'token': str(token.token)})
        )
        # Envoi du mail
        send_mail(
            subject="Réinitialisation de votre mot de passe",
            message=f"Bonjour {user.username},\nCliquez sur ce lien pour réinitialiser votre mot de passe:\n{reset_link}\nCe lien est valide 1h.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        return JsonResponse({'status': 'success', 'message': 'Email envoyé avec succès !'})
    return JsonResponse({'status': 'error', 'message': 'Requête invalide'})



@login_required
@admin_required
def modifier_utilisateur(request, user_id):
<<<<<<< HEAD
    """
    Modification d'un utilisateur (admin seulement)
    """
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user.employe, user=user)

        if form.is_valid():
            form.save()
=======

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            user = form.save(commit=False)

            password = form.cleaned_data.get("password")

            if password:
                user.set_password(password)

            user.save()

>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
            messages.success(request, "Utilisateur modifié avec succès")
            return redirect('users:liste_utilisateurs')

    else:
<<<<<<< HEAD
        form = UserProfileForm(instance=user.employe, user=user)
=======
        form = UserProfileForm(instance=user)
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad

    return render(request, "utilisateurs/modifier_utilisateur.html", {
        "form": form,
        "user_obj": user
    })


@login_required
@admin_required
def supprimer_utilisateur(request, user_id):
    """
    Suppression (soft delete) d'un utilisateur (admin seulement)
<<<<<<< HEAD
    Désactive le compte au lieu de le supprimer, ce qui rend le bouton 
    "Créer un compte" disponible à nouveau dans la liste des employés.
=======
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
    """
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        user.est_actif = False  # Désactive le compte au lieu de le supprimer
        user.save()
        messages.success(request, f"Utilisateur {user.username} désactivé avec succès.")
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "message": "Méthode non autorisée"}, status=405)



@login_required
def dashboard(request):
    user = request.user

    stats = {
        'users': 0,
        'clients': 0,
        'activites': 0,
        'prospects': 0,
        'mes_prospects': 0,
        'mes_conversions': 0,
        'total_converti': 0,
        'conversion_stats': [],
        'taux_conversion': 0,
        'top_techniciens': [],

        # TECHNICIEN
        'activites_terminees': 0,
        'activites_en_cours': 0,
        'activites_planifiees': 0,
        'activites_en_attente': 0,
        'taux_realisation': 0,
    }

    # =========================
    # ADMIN / SUPERVISEUR
    # =========================
    if user.user_type in ['admin', 'superviseur']:

        stats['users'] = User.objects.count()
<<<<<<< HEAD
        stats['clients'] = Client.objects.filter(est_supprime=False).count()
=======
        stats['clients'] = Client.objects.count()
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
        stats['activites'] = Activite.objects.count()
        stats['prospects'] = Prospect.objects.count()

        stats['total_converti'] = Prospect.objects.filter(statut="converti").count()

        total = stats['prospects']
        converti = stats['total_converti']
        stats['taux_conversion'] = round((converti / total) * 100, 1) if total else 0

        stats['conversion_stats'] = (
            Prospect.objects.filter(statut="converti")
<<<<<<< HEAD
            .values('commercial__employe__nom', 'commercial__employe__prenom')
=======
            .values('commercial__nom', 'commercial__prenom')
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        stats['top_techniciens'] = (
            Technicien.objects.annotate(
                total_activites=Count('activites')
            ).order_by('-total_activites')[:3]
        )

    # =========================
<<<<<<< HEAD
    # RESSOURCES HUMAINES
    # =========================
    if user.user_type in ['admin', 'rh']:

        from employes.models import Employe

        stats['total_employes'] = Employe.objects.count()
        stats['employes_actifs'] = Employe.objects.filter(statut='Actif').count()
        stats['techniciens'] = Technicien.objects.count()
        stats['commerciaux'] = Commercial.objects.count()

        # Employés nouveaux ce mois (approximation)
        from django.utils import timezone
        import datetime
        debut_mois = timezone.now().replace(day=1)
        stats['nouveaux_employes'] = Employe.objects.filter(date_embauche__gte=debut_mois).count()

        stats['employes_inactifs'] = Employe.objects.filter(statut='Inactif').count()

    # =========================
=======
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
    # TECHNICIEN
    # =========================
    elif user.user_type == 'technicien':

<<<<<<< HEAD
        if user.employe and hasattr(user.employe, 'technicien_profile') and user.employe.technicien_profile:

            qs = Activite.objects.filter(
                techniciens=user.employe.technicien_profile
=======
        if hasattr(user, 'technicien') and user.technicien:

            qs = Activite.objects.filter(
                techniciens=user.technicien
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
            )

            stats['activites'] = qs.count()
            stats['activites_terminees'] = qs.filter(statut="termine").count()
            stats['activites_en_cours'] = qs.filter(statut="en_cours").count()
            stats['activites_planifiees'] = qs.filter(statut="planifie").count()
            stats['activites_en_attente'] = qs.filter(statut="en_attente").count()

            total = stats['activites']
            termine = stats['activites_terminees']
            stats['taux_realisation'] = round((termine / total) * 100, 1) if total else 0

    # =========================
    # COMMERCIAL
    # =========================
    elif user.user_type == 'commercial':

<<<<<<< HEAD
        if user.employe and hasattr(user.employe, 'commercial_profile') and user.employe.commercial_profile:

            stats['clients'] = Client.objects.filter(
                commercial=user.employe.commercial_profile,
                est_supprime=False
            ).count()

            stats['mes_prospects'] = Prospect.objects.filter(
                commercial=user.employe.commercial_profile
            ).count()

            stats['mes_conversions'] = Prospect.objects.filter(
                commercial=user.employe.commercial_profile,
=======
        if hasattr(user, 'commercial') and user.commercial:

            stats['clients'] = Client.objects.filter(
                commercial=user.commercial
            ).count()

            stats['mes_prospects'] = Prospect.objects.filter(
                commercial=user.commercial
            ).count()

            stats['mes_conversions'] = Prospect.objects.filter(
                commercial=user.commercial,
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
                statut="converti"
            ).count()

    return render(request, 'utilisateurs/dashboard.html', {
        'stats': stats,
        'user': user
    }) 
    
    
    
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('users:login')