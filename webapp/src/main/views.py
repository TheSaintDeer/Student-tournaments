from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'main/index.html')

def freepage(request):
    return render(request, 'main/freepage.html')

def login(request):
    return render(request, 'main/login.html')

def news(request):
    return render(request, 'main/news.html')

def tournaments(request):
    return render(request, 'main/tournaments.html')

def notification(request):
    return render(request, 'main/notification.html')