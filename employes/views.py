from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Employe
from .forms import EmployeForm


@login_required
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

    context = {
        "page_obj": page_obj,
        "search": search,
        "total_employes": total_employes,
    }

    return render(request, "employes/liste_employes.html", context)


@login_required
def ajouter_employe(request):

    if request.method == "POST":

        form = EmployeForm(request.POST, request.FILES)

        if form.is_valid():

            employe = form.save()

            messages.success(
                request,
                f"L'employé {employe.nom} {employe.prenom} a été ajouté avec succès.",
            )

            return redirect("liste_employes")

        else:

            messages.error(request, "Veuillez corriger les erreurs du formulaire.")

    else:

        form = EmployeForm()

    context = {"form": form, "titre": "Ajouter un employé"}

    return render(request, "employes/ajout_employes.html", context)
