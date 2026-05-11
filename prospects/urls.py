from django.urls import path
from . import views

app_name = "prospects"

urlpatterns = [
    path('prospects/', views.list_prospects, name='list_prospects'),
    path('ajouter/', views.add_prospect, name='add_prospect'),
    path('<int:id>/', views.detail_prospect, name='detail_prospect'),
    path("edit/<int:id>/", views.edit_prospect, name="edit_prospect"),
    path('<int:id>/delete/', views.delete_prospect, name='delete_prospect'),
    path('convertir/<int:prospect_id>/', views.convertir_prospect_en_client, name='convertir_prospect'),
    
]