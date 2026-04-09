from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import TypeContrat

# ================= LISTE =================
def liste_type_contrat(request):
    types = TypeContrat.objects.all().order_by('-id')
    return render(request, 'type_contrats/liste.html', {'types': types})


# ================= AJOUT =================
def ajouter_type_contrat(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')

        TypeContrat.objects.create(
            nom=nom,
            description=description
        )

        messages.success(request, "✅ Type de contrat ajouté avec succès")
        return redirect('type_contrat:liste_type')

    return render(request, 'type_contrats/ajouter.html')


# ================= MODIFIER =================
def modifier_type_contrat(request, type_id):
    type_contrat = get_object_or_404(TypeContrat, id=type_id)

    if request.method == 'POST':
        type_contrat.nom = request.POST.get('nom')
        type_contrat.description = request.POST.get('description')
        type_contrat.save()

        messages.success(request, "✅ Type de contrat modifié avec succès")
        return redirect('type_contrat:liste_type')

    return render(request, 'type_contrats/modifier.html', {
        'type': type_contrat
    })

# ================= SUPPRIMER =================
def supprimer_type_contrat(request, type_id):
    type_contrat = get_object_or_404(TypeContrat, id=type_id)
    type_contrat.delete()

    messages.success(request, "🗑️ Supprimé avec succès")
    return redirect('type_contrat:liste_type')