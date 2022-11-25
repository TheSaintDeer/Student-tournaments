from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from main.models import Player, Round

class CreateRoundForm(forms.ModelForm):

    class Meta:
        model = Round
        fields = '__all__'