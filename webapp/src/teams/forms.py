from django import forms
from main.models import Player

class PlayerForTeamForm(forms.Form):

    def __init__(self, players_queryset, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['player'] = forms.ModelChoiceField(queryset=players_queryset, empty_label="Choose a player")

    player = forms.ModelChoiceField(queryset=Player.objects.all())
