from django import forms
from .models import Employe, Poste


class PosteForm(forms.ModelForm):
    class Meta:
        model = Poste
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Nom du poste'}),
        }
        labels = {
            'nom': 'Poste *',
        }


class EmployeForm(forms.ModelForm):

    class Meta:
        model = Employe
        fields = [
            'photo',
            'nom',
            'prenom',
            'sexe',
            'date_naissance',
            'telephone',
            'email',
            'adresse',
            'quartier',
            'poste',
            'date_embauche',
            'statut',
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Prénom'}),
            'sexe': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Téléphone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Email'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3, 'placeholder': 'Adresse'}),
            'quartier': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Quartier'}),
            'poste': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'date_embauche': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}),
            'statut': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'photo': forms.FileInput(attrs={'class': 'form-control form-control-sm'}),
        }
        labels = {
            'nom': 'Nom *',
            'prenom': 'Prénom *',
            'sexe': 'Sexe *',
            'date_naissance': 'Date de naissance',
            'telephone': 'Téléphone *',
            'email': 'Email',
            'adresse': 'Adresse',
            'quartier': 'Quartier',
            'poste': 'Poste',
            'date_embauche': 'Date d\'embauche',
            'statut': 'Statut *',
            'photo': 'Photo',
        }

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone', '').strip()
        normalized = ''.join(ch for ch in telephone if ch.isdigit())

        if normalized.startswith('224'):
            normalized = normalized[3:]

        if not normalized.isdigit() or len(normalized) != 9:
            raise forms.ValidationError(
                "Le numéro doit contenir 9 chiffres. Exemple : 612345678"
            )

        if normalized[:2] not in ['61', '62', '65', '66']:
            raise forms.ValidationError(
                "Le numéro doit commencer par 61, 62, 65 ou 66."
            )

        return normalized

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            default_class = field.widget.attrs.get('class', '')
            if not default_class:
                if isinstance(field.widget, (forms.Select, forms.ClearableFileInput)):
                    default_class = 'form-select form-select-sm' if not isinstance(field.widget, forms.ClearableFileInput) else 'form-control form-control-sm'
                else:
                    default_class = 'form-control form-control-sm'

            if self.is_bound and self[name].errors:
                default_class += ' is-invalid'

            field.widget.attrs['class'] = default_class.strip()

            if field.required:
                field.widget.attrs.setdefault('required', 'required')

