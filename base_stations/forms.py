from django import forms
from .models import BaseStation

class BaseStationForm(forms.ModelForm):
    class Meta:
        model = BaseStation
        fields = ['nom','description']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la base station'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
        }