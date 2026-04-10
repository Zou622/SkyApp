from django.urls import path

from . import views

app_name = 'rapportActivites'

urlpatterns = [
    path('activites/technicien/<int:technicien_id>/', views.liste_activites_technicien, name='liste_activites_technicien_avec_id'),
    path('activites/technicien/', views.liste_activites_technicien, name='liste_activites_technicien'),
    path('activite/<int:activite_id>/demarrer/', views.demarrer_activite, name='demarrer_activite'),
    path('rapport/<int:activite_id>/', views.creer_rapport, name='creer_rapport'),
    path('rapport/detail/<int:pk>/', views.detail_rapport, name='detail_rapport'),
    path('rapports/', views.liste_rapports, name='liste_rapports'),
    #path('rapports/export/', views.export_rapports_excel, name='export_rapports_excel'),

]