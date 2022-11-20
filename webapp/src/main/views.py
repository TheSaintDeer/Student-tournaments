from django.shortcuts import render, loader, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login
from urllib import request
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django import http

from main.forms import NewUserForm, UpdateUserForm, UpdatePlayerForm, PostForm
from main.models import Tournament, Team, Player, Post
from django.contrib.auth.models import User
import json


def index(request):
    return render(request, 'main/index.html')


@login_required
def profile(request):
    player = Player.objects.get(id=request.user.id)
    team_list = player.teams.all()

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdatePlayerForm(request.POST, request.FILES, instance=player)
        post_form = PostForm()

        # if user_form.is_valid() and profile_form.is_valid():
        if user_form.is_valid():
            user_form.save()
            profile_form.save()
            # profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect("main:profile")
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdatePlayerForm(instance=player)
    return render(request, 'profile/profile.html',
                  {'user_form': user_form, 'team_list': team_list, 'profile_form': profile_form, 'player': player})


@login_required
@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        player = Player.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdatePlayerForm(request.POST, request.FILES, instance=player)
        response_data = {}
        response_data['result'] = 'Create post successful!'
        print(request.POST)

        if profile_form.is_valid():
            profile_form.save()

        if user_form.is_valid():
            user_form.save()

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        response_data = {}
        print(post_text)
        post = Post(text=post_text, author=request.user)
        post.save()

        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = post.pk
        response_data['text'] = post.text

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
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