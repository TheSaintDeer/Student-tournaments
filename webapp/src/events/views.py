from django.shortcuts import render
from django.http import HttpResponse
from main.models import Tournament

def index(request):
    all_tournaments = Tournament.objects.all
    return render(request, 'events/base.html', {'all_tournaments':all_tournaments})
