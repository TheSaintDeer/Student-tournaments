from django.shortcuts import render, get_object_or_404
from main.models import Tournament, Team

# Create your views here.

def tournaments(request):
    tournament_list = Tournament.objects.all()[:5]
    context = {
        'tournament_list': tournament_list,
    }
    return render(request, 'tournaments/tournaments.html', context)

def detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    team_list = Team.objects.filter(tournament=tournament)
    return render(request, 'tournaments/detail.html', {'tournament': tournament, 'team_list': team_list})