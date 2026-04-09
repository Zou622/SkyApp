from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import BaseStation
from .forms import BaseStationForm

# Liste
def liste_base_stations(request):
    base_stations = BaseStation.objects.all().order_by('-id')
    return render(request, 'base_Stations/liste_base_stations.html', {'base_stations': base_stations})

# Ajouter
def ajouter_base_station(request):
    if request.method == "POST":
        form = BaseStationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Base Station ajoutée avec succès !")
            return redirect('base_stations:liste_base_stations')
        else:
            messages.error(request, "Erreur lors de l'ajout")
    else:
        form = BaseStationForm()
    return render(request, 'base_Stations/ajouter_base_station.html', {'form': form})

# Modifier
def modifier_base_station(request, bs_id):
    bs = get_object_or_404(BaseStation, id=bs_id)
    if request.method == "POST":
        form = BaseStationForm(request.POST, instance=bs)
        if form.is_valid():
            form.save()
            messages.success(request, "Base Station modifiée avec succès !")
            return redirect('base_stations:liste_base_stations')
        else:
            messages.error(request, "Erreur lors de la modification")
    else:
        form = BaseStationForm(instance=bs)
    return render(request, 'base_Stations/modifier_base_station.html', {'form': form, 'bs': bs})

# Supprimer
def supprimer_base_station(request, bs_id):
    bs = get_object_or_404(BaseStation, id=bs_id)
    bs.delete()
    messages.success(request, "Base Station supprimée avec succès !")
    return redirect('base_stations:liste_base_stations')