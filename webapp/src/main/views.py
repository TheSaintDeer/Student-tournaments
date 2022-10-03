from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'main/index.html')

def login(request):
    return render(request, 'login/index.html')

def tournaments(request):
    return render(request, 'tournaments/index.html')

def notification(request):
    return render(request, 'notification/index.html')

def teams(request):
    return render(request, 'teams/index.html')