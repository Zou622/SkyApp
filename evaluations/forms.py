from django import forms
from .models import Evaluation


class EvaluationForm(forms.ModelForm):

    class Meta:
        model = Evaluation
        exclude = ["evaluateur", "score_total"]
