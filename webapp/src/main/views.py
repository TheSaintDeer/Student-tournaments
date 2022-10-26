from django.shortcuts import render, loader, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login
from urllib import request
from django.contrib.auth.decorators import login_required
from django import http

from main.forms import NewUserForm
from main.models import Tournament, Team, Player
from django.contrib.auth.models import User

def index(request):
    return render(request, 'main/index.html')

@login_required
def profile(request):
    team_list = Player.objects.get(pk = request.user.pk).teams.all()
    return render(request, 'profile/profile.html', {'team_list': team_list})

def notification(request):
    return render(request, 'notification/index.html')

def registration_request(request):
        if request.method == "POST":
            form = NewUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                player = Player.objects.create(user = user)
                login(request, user)
                messages.success(request, "Registration successful." )
                return redirect("main:home")
            messages.error(request, "Unsuccessful registration. Invalid information.")
            return render (request=request, template_name="registration/registration.html", context={"register_form":form})
            
        elif request.method == "GET":
            form = NewUserForm()
            return render (request=request, template_name="registration/registration.html", context={"register_form":form})

