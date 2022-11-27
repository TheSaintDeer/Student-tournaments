from django.shortcuts import render, loader, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import login
from urllib import request
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django import http
from rest_framework import status

from main.forms import NewUserForm, UpdateUserForm, UpdatePlayerForm
from main.models import Tournament, Team, Player
from django.contrib.auth.models import User
import json


def index(request):
    return render(request, 'main/index.html')


def user_detail(request, user_id):
    user = User.objects.get(id = user_id)
    player = Player.objects.get(user = user)
    return render(request, 'main/user_detail.html', {'user': user, 'player': player})


@login_required
def profile(request):
    player = Player.objects.get(id=request.user.id)
    team_list = player.teams.all()

    if request.method == 'POST':
        # user_form = UpdateUserForm(request.POST, instance=request.user)
        # profile_form = UpdatePlayerForm(request.POST, request.FILES, instance=player)
        # post_form = PostForm()

        # # if user_form.is_valid() and profile_form.is_valid():
        # if user_form.is_valid():
        #     user_form.save()
        #     profile_form.save()
        #     # profile_form.save()
        #     messages.success(request, 'Your profile is updated successfully')
            return redirect("main:profile")
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdatePlayerForm(instance=player)
    return render(request, 'profile/profile.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'player': player})





@login_required
@csrf_protect
def update_profile(request):
    if request.method == 'POST':
        player = Player.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdatePlayerForm(request.POST, request.FILES, instance=player)
        print(request.POST)

        if profile_form.is_valid():
            profile_form.save()

        if user_form.is_valid():
            user_form.save()

        return JsonResponse(
            data=None,
            safe=False,
            content_type="application/json",
            status=status.HTTP_200_OK
        )
    else:
        return JsonResponse(
            data=None,
            safe=False,
            content_type="application/json",
            status=status.HTTP_400_BAD_REQUEST
        )

def notification(request):
    return render(request, 'notification/index.html')


def registration_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            player = Player.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
        return render(request=request, template_name="registration/registration.html", context={"register_form": form})

    elif request.method == "GET":
        form = NewUserForm()
        return render(request=request, template_name="registration/registration.html", context={"register_form": form})