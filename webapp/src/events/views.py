from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from main.models import Tournament, Team

def index(request):
    all_tournaments = Tournament.objects.all()
    return render(request, 'events/events.html', {'all_tournaments':all_tournaments})

def detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    team_list = Team.objects.filter(tournament=tournament)
    return render(request, 'events/detail.html', {'tournament': tournament, 'team_list': team_list})

def create(request):
    if request.method == 'POST':
        aux = get_user_model()
        user_list = User.objects.all()
        name = request.POST['eventName']
        description = request.POST['eventDesc']
        logo = request.POST['eventLogo']
        owner = request.POST['eventOwner']
        count_teams = request.POST['eventTeams']
        count_players = request.POST['eventPlayers']
        reward = request.POST['eventReward']
        state = request.POST['eventStatus']
        for usr in user_list:
            if owner == str(usr):
                new_event = Tournament(name=name, description=description, logo=logo, owner=usr, count_teams=int(count_teams),
                                       count_players_in_team=int(count_players), reward=int(reward), state=state)
                new_event.save()
    return render(request, 'events/create.html')
