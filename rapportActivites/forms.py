from django import forms
from rapportActivites.models import RapportActivite


class RapportActiviteForm(forms.ModelForm):

    class Meta:
        model = RapportActivite
        fields = [
            'date_intervention_reelle',
            'heure_debut_reelle',
            'heure_fin_reelle',
            'travaux_realises',
            'difficultes_rencontrees',
            'solutions_apportees',
            'etat_avant',
            'etat_apres',
            'equipements_utilises',
            'materiel_consomme',
            'materiel_remplace',
            'parametres_configures',
            'qualite_signal',
            'debit_constate',
            'client_present',
            'satisfaction_client',
            'commentaire_client',
            'recommandations',
            'prochaine_action',
            'date_prochaine_intervention',
            'photo_avant',
            'photo_apres',
            'document_joint',
            'description',
            'point_de_depart',
            'nombre_de_joinbox_poser',
            'type_de_brain',
            'quel_joinbox',
            'tube',
            'quel_brain',
            'photo_appareils_connecte',
            'plainte_client',
            'photo_ping'
        ]

    def __init__(self, *args, **kwargs):

        self.activite = kwargs.pop('activite', None)

        super().__init__(*args, **kwargs)

        if self.activite:

            # ✅ sécuriser
            type_activite = self.activite.type_activite.lower().strip()

            champs_par_type = {

                "installation": [
                    'date_intervention_reelle',
                    'heure_debut_reelle',
                    'heure_fin_reelle',
                    'description',
                    'travaux_realises',
                    'equipements_utilises',
                    'parametres_configures',
                    'photo_avant',
                    'photo_apres'
                ],

                "maintenance": [
                    'date_intervention_reelle',
                    'heure_debut_reelle',
                    'heure_fin_reelle',
                    'travaux_realises',
                    'materiel_remplace',
                    'solutions_apportees',
                    'photo_avant',
                    'photo_apres',
                    'description'
                ],

                "survey": [
                    'date_intervention_reelle',
                    'heure_debut_reelle',
                    'heure_fin_reelle',
                    'travaux_realises',
                    'etat_avant',
                    'difficultes_rencontrees',
                    'photo_avant',
                    'description'
                ],

                "investigation": [
                    'date_intervention_reelle',
                    'heure_debut_reelle',
                    'heure_fin_reelle',
                    'travaux_realises',
                    'difficultes_rencontrees',
                    'solutions_apportees'
                ],
                
                "tirage_fo":[
                    'date_intervention_reelle',
                    'heure_debut_reelle',
                    'heure_fin_reelle',
                    'point_de_depart',
                    'nombre_de_joinbox_poser',
                    'type_de_brain',
                    'photo_apres',
                ],
                
                "raccordement":[
                    'date_intervention_reelle',
                    'heure_debut_reelle',
                    'heure_fin_reelle',
                    'quel_joinbox',
                    'tube',
                    'quel_brain',
                    'photo_avant',
                    'photo_apres',
                    'description'
                ],
                
                'remplacement':[
                    'date_intervention_reelle',
                    'heure_debut_reelle',
                    'heure_fin_reelle',
                    'description',
                    'photo_avant',
                    'photo_apres'
                ],
                
                'noc support':[
                    'date_intervention_reelle',
                    'heure_debut_reelle',
                    'heure_fin_reelle',
                    'description',
                    'plainte_client',
                    'photo_ping'
                    'photo_appareils_connecte'
                ],
                
                'autre':[
                    'date_intervention_reelle',
                    'heure_debut_reelle',
                    'heure_fin_reelle',
                    'description',
                    'photo_avant',
                    'photo_apres',
                    'travaux_realises',
                    'difficultes_rencontrees',
                    'solutions_apportees'
                ]
                
            }

            champs_autorises = champs_par_type.get(type_activite, [])

            # supprimer les champs non utiles
            for field in list(self.fields.keys()):
                if field not in champs_autorises:
                    self.fields.pop(field)
                    
                    
            # ajouter style bootstrap
            for name, field in self.fields.items():

                if hasattr(field, 'widget'):

                    if field.widget.__class__.__name__ == 'CheckboxInput':
                        field.widget.attrs.update({'class': 'form-check-input'})
                    else:
                        field.widget.attrs.update({'class': 'form-control'})