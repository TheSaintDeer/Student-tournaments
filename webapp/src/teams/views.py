from django.shortcuts import render, get_object_or_404
from main.models import Team, Player

# Create your views here.
def detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    players_list = Player.objects.filter(team=team_id)
    return render(request, 'teams/detail.html', {'team': team, 'players_list': players_list})