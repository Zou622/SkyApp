from django import forms
from .models import Objectif


class ObjectifForm(forms.ModelForm):

    class Meta:

        model = Objectif

        fields = "__all__"

        widgets = {
            "date_debut": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "date_fin": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "titre": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "pourcentage_realisation": forms.NumberInput(
                attrs={"class": "form-control", "min": 0, "max": 100}
            ),
            "employe": forms.Select(attrs={"class": "form-select"}),
            "statut": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre le champ obligatoire (par défaut il l'est déjà, mais on s'assure)
        self.fields["pourcentage_realisation"].required = True
        # Ajouter un label clair
        self.fields["pourcentage_realisation"].label = "Pourcentage de réalisation (%)"
        # Ajouter un message d'aide
        self.fields["pourcentage_realisation"].help_text = (
            "Entrez un nombre entre 0 et 100"
        )
