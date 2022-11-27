from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from main.models import Team, Player, Tournament
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import http
from django.contrib import messages
from teams.forms import PlayerForTeamForm
from rest_framework.exceptions import NotFound
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def detail(request, team_id):
    current_team = get_object_or_404(Team, pk=team_id)
    players_list = Player.objects.filter(teams__id = team_id)
    return render(request, 'teams/detail.html', {'team': current_team, 'players_list': players_list})

@login_required
def add_player(request, team_id):

    if request.method == 'POST':
        form = PlayerForTeamForm(team_id, request.POST)
        team = Team.objects.get(id = team_id)
        tournament = Tournament.objects.get(id = team.tournament.id)
        player_to_add = Player.objects.get(id = request.POST['player'])
        amount_of_players = Player.objects.filter(teams__id = team.id).count()

        # if request user if a team owner, than he can add players to this team
        if (team.owner.pk == request.user.id): 

            # TODO check if player exist in other teams of this tour
            for item in tournament.team_set.all():
                list_of_players = list(item.player_set.all())
                if player_to_add in list_of_players:
                    return http.HttpResponseNotFound("Player already has a team!")

            # check if amount of players in team is less than max players in team in this tournament
            if (amount_of_players < team.tournament.players_in_team):             
                if form.is_valid():

                    # add player to team
                    player_to_add.teams.add(team)               
                    print(str(player_to_add) + ' was added to team ' + str(team))


                    # redirect back to team detail page
                    next = request.POST.get('next','/')
                    return http.HttpResponseRedirect(next)
            else:
                return http.HttpResponseNotFound("Too much players in team.")

        # if request user is not an owner, than response forbidden
        return http.HttpResponseNotFound("You are not a team owner.")

    else:
        form = PlayerForTeamForm(team_id=team_id)
    return render(request, 'teams/player_for_team.html', {'form': form})


class TeamsCreateView(LoginRequiredMixin, CreateView):
    model = Team
    template_name = 'teams/team_create_form.html'
    fields = ['name', 'logo']

    def form_valid(self, form):
        tournament_id = self.kwargs['pk']
        current_tournament = Tournament.objects.get(pk = tournament_id)
    
        if Team.objects.filter(tournament = current_tournament).count() < current_tournament.teams_number:

            # TODO check if owner exist in other teams of this tour
            player = Player.objects.get(pk = self.request.user.pk)
            if (Player.objects.filter(teams__tournament = current_tournament).contains(player)):
                return http.HttpResponseForbidden('Player already has a team.')


            form.instance.owner = self.request.user
            form.instance.tournament = current_tournament
            super().form_valid(form)
            player.teams.add(self.object.id)
            return super().form_valid(form)
            
        else:
            return http.HttpResponseForbidden('too much teams!')

    def get_success_url(self):
            return reverse("tournaments:detail", kwargs={'tournament_id': self.kwargs['pk']})


class TeamsDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = 'teams/team_confirm_delete.html'
    success_url = '/tournaments'

    def form_valid(self, form):
        owner = Team.objects.get(pk = self.kwargs['pk']).owner
        if owner == self.request.user:
            success_url = self.get_success_url()
            self.object.delete()
            return http.HttpResponseRedirect(self.success_url)
        else:
            return http.HttpResponseForbidden('no permissions!')

