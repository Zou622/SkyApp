from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from employes.models import Employe
from objectifs.models import Objectif

from .models import Evaluation
from .forms import EvaluationForm


@login_required
def liste_evaluations(request):

    evaluations = Evaluation.objects.filter(evaluateur=request.user).order_by(
        "-date_evaluation"
    )

    context = {"evaluations": evaluations}

    return render(request, "evaluations/liste_evaluation.html", context)


@login_required
def ajouter_evaluation(request):

    if request.method == "POST":

        form = EvaluationForm(request.POST)

        if form.is_valid():

            evaluation = form.save(commit=False)

            evaluation.evaluateur = request.user

            evaluation.save()

            messages.success(request, "Evaluation ajoutée.")

            return redirect("evaluations:liste_evaluations")

    else:
        form = EvaluationForm()

    context = {"form": form}

    return render(request, "evaluations/ajout_evaluation.html", context)


from django.shortcuts import get_object_or_404, redirect, render


@login_required
def modifier_evaluation(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk)

    employes = Employe.objects.all()
    objectifs = Objectif.objects.filter(employe=evaluation.employe)

    if request.method == "POST":

        evaluation.employe_id = request.POST.get("employe")
        evaluation.objectif_id = request.POST.get("objectif")
        evaluation.commentaire = request.POST.get("commentaire")

        # ✅ FIX IMPORTANT
        evaluation.ponctualite = int(request.POST.get("ponctualite") or 0)
        evaluation.discipline = int(request.POST.get("discipline") or 0)
        evaluation.performance = int(request.POST.get("performance") or 0)

        evaluation.save()

        messages.success(request, "Évaluation modifiée avec succès.")
        return redirect("evaluations:liste_evaluations")

    return render(
        request,
        "evaluations/modifier_avaluation.html",
        {
            "evaluation": evaluation,
            "employes": employes,
            "objectifs": objectifs,
        },
    )


@login_required
def detail_evaluation(request, pk):

    evaluation = get_object_or_404(Evaluation, pk=pk)

    context = {"evaluation": evaluation}

    return render(request, "evaluations/detail_evaluation.html", context)


@login_required
def supprimer_evaluation(request, pk):

    evaluation = get_object_or_404(Evaluation, pk=pk, evaluateur=request.user)

    evaluation.delete()

    messages.success(request, "Evaluation supprimée.")

    return redirect("evaluations:liste_evaluations")
