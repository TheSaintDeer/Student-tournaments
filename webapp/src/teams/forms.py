from django import forms
from main.models import Player

class PlayerForTeamForm(forms.Form):

    def __init__(self, team_id, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['player'] = forms.ModelChoiceField(queryset=Player.objects.exclude(teams__id = team_id), empty_label="Choose a player")

    player = forms.ModelChoiceField(queryset=Player.objects.all())
