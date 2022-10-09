from rest_framework import serializers
from main.models import Tournament, Team, Player

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['name','description','owner']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name','tournament','players']

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['user','team']