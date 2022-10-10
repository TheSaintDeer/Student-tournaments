from django.shortcuts import render, get_object_or_404
from main.models import Tournament, Team

def index(request):
    all_tournaments = Tournament.objects.all()
    return render(request, 'events/events.html', {'all_tournaments':all_tournaments})

def detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    team_list = Team.objects.filter(tournament=tournament)
    return render(request, 'events/detail.html', {'tournament': tournament, 'team_list': team_list})
