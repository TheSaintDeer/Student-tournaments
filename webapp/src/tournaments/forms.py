from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError

from main.models import Player, Round, Match, Tournament

class ApproveTournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['approved_by_admin']

class CreateRoundForm(forms.ModelForm):

    def __init__(self, tournament, *args,**kwargs):
                    super().__init__(*args,**kwargs)
                    self.instance.tournament = tournament

    class Meta:
        model = Round
        fields = ['reward_points']



def create_match_form(teams_queryset, round):

    class CreateMatchForm(forms.ModelForm):

        def __init__(self, *args,**kwargs):
                super().__init__(*args,**kwargs)
                self.fields['blue'] = forms.ModelChoiceField(queryset=teams_queryset, empty_label="Choose a blue team", required=True)
                self.fields['red'] = forms.ModelChoiceField(queryset=teams_queryset, empty_label="Choose a red team", required=True)
                self.instance.round = round
        class Meta:
            model = Match
            fields = ['blue', 'red', 'blue_score', 'red_score']
        
        def clean(self):

            cleaned_data = super().clean()

            blue = cleaned_data.get("blue")
            red = cleaned_data.get("red")

            if blue is None or red is None:
                raise ValidationError("Wrong match configuration.")

            if blue == red:
                raise ValidationError("Team cant have a match vs itself.")

            return cleaned_data


    return CreateMatchForm
