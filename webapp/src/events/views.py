from django.shortcuts import render
from django.http import HttpResponse
from .models import Event

def index(request):
    all_tournaments = Event.objects.all
    return render(request, 'events/base.html', {'all_tournaments':all_tournaments})
