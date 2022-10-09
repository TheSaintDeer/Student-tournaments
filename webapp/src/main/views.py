from django.shortcuts import render, loader, get_object_or_404
from django.http import HttpResponse

from main.models import Tournament, Team, Player
from django.contrib.auth.models import User

def index(request):
    return render(request, 'main/index.html')

def login(request):
    return render(request, 'login/index.html')

def profile(request):
    # return render(request, 'profile/profile.html')
    # team_list = Team.objects.all()
    team_list = Team.objects.filter(players__id = request.user.id)
    
    return render(request, 'profile/profile.html', {'team_list': team_list})

def notification(request):
    return render(request, 'notification/index.html')
