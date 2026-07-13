from pyexpat.errors import messages

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from activites.models import Activite
from objectifs.models import Objectif
from techniciens.models import Technicien
from .forms import ObjectifForm
from employes.models import Employe
from django.contrib import messages


@login_required
def liste_objectifs(request):

    objectifs = Objectif.objects.select_related("employe").order_by("-created_at")

    context = {"objectifs": objectifs}

    return render(request, "objectifs/liste_objectifs.html", context)


@login_required
def ajouter_objectif(request, employe_id=None):

    employe = None

    if employe_id:
        employe = get_object_or_404(Employe, id=employe_id)

    if request.method == "POST":

        form = ObjectifForm(request.POST)

        if form.is_valid():

            objectif = form.save(commit=False)

            if employe:
                objectif.employe = employe

            objectif.save()
            messages.success(request, "Objectif ajouté avec succès.")
            return redirect("objectifs:liste_objectif")

    else:

        initial = {}

        if employe:
            initial["employe"] = employe

        form = ObjectifForm(initial=initial)

    context = {"form": form, "employe": employe, "titre": "Ajouter Objectif"}

    return render(request, "objectifs/ajouter_objectis.html", context)


@login_required
def detail_objectif(request, pk):

    objectif = get_object_or_404(Objectif, pk=pk)

    return render(request, "objectifs/detail_objectifs.html", {"objectif": objectif})


@login_required
def modifier_objectif(request, pk):

    objectif = get_object_or_404(Objectif, pk=pk)

    if request.method == "POST":

        form = ObjectifForm(request.POST, instance=objectif)

        if form.is_valid():

            form.save()
            messages.success(request, "Objectif modifier avec succès.")
            return redirect("objectifs:liste_objectif")

    else:

        form = ObjectifForm(instance=objectif)

    context = {"form": form, "objectif": objectif, "titre": "Modifier Objectif"}

    return render(request, "objectifs/ajouter_objectis.html", context)


@login_required
def supprimer_objectif(request, pk):

    objectif = get_object_or_404(Objectif, pk=pk)

    objectif.delete()

    return redirect("objectifs:liste_objectif")



###Vue pour recupérer les objectifs d'un employé
def get_objectifs_by_employe(request):
    employe_id = request.GET.get("employe_id")

    objectifs = Objectif.objects.filter(employe_id=employe_id).values("id", "titre")

    return JsonResponse(list(objectifs), safe=False)
