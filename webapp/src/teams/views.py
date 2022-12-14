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

# Max Koval (xkoval20)
def detail(request, team_id):
    current_team_q = Team.objects.filter(id=team_id)
    if not current_team_q.exists():
        return redirect("tournaments:tournaments")
    current_team = current_team_q.first()

    players_list = Player.objects.filter(teams__id = team_id)
    return render(request, 'teams/detail.html', {'team': current_team, 'players_list': players_list})

# Max Koval (xkoval20)
@login_required
def add_player(request, team_id):

    team_q = Team.objects.filter(id = team_id)
    if not team_q.exists():
        return redirect("tournaments:tournaments")
    team = team_q.first()

    players_queryset = Player.objects.exclude(teams__id = team_id)

    if request.method == 'POST':
        
        form = PlayerForTeamForm(players_queryset, request.POST)
        tournament_q = Tournament.objects.filter(id = team.tournament.id)
        if not tournament_q.exists():
            return redirect("tournaments:tournaments")
        tournament = tournament_q.first()
        
        player_to_add_q = Player.objects.filter(id = request.POST['player'])
        if not player_to_add_q.exists():
            return redirect("tournaments:tournaments")
        player_to_add = player_to_add_q.first()

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
        form = PlayerForTeamForm(players_queryset)
    return render(request, 'teams/add_player_to_team.html', {'form': form})

# Max Koval (xkoval20)
def remove_player(request, team_id):

    team_q = Team.objects.filter(id = team_id)
    if not team_q.exists():
        return redirect("tournaments:tournaments")
    team = team_q.first()

    players_queryset = team.player_set.all()

    if request.method == 'POST':
       
        form = PlayerForTeamForm(players_queryset, request.POST)

        # if request user if a team owner, than he can remove players from this team
        if (team.owner.pk == request.user.id) or request.user.is_superuser: 
         
            if form.is_valid():

                player_to_remove_q = Player.objects.filter(id = request.POST['player'])
                if not player_to_remove_q.exists():
                    return redirect("tournaments:tournaments")
                player_to_remove = player_to_remove_q.first()

                if request.user == player_to_remove.user:
                    messages.warning(request, "You cant remove team owner.")
                    return render(request, 'teams/remove_player_from_team.html', {'form': form})

                # remove player from team
                player_to_remove.teams.remove(team)               
                print(str(player_to_remove) + ' was removed from team ' + str(team))

                return redirect("teams:detail", team_id=team_id)
            else:
                messages.warning(request, "Too much players in team.")
                return render(request, 'teams/remove_player_from_team.html', {'form': form})

        # if request user is not an owner, than response forbidden
        messages.warning(request, "You are not a team owner.")
        return render(request, 'teams/remove_player_from_team.html', {'form': form})

    else:
        form = PlayerForTeamForm(players_queryset=players_queryset)
    return render(request, 'teams/add_player_to_team.html', {'form': form})

# Max Koval (xkoval20)
class TeamsCreateView(LoginRequiredMixin, CreateView):
    model = Team
    template_name = 'teams/team_create_form.html'
    fields = ['name', 'logo']
    success_url = '/tournaments'

    def form_valid(self, form):
        tournament_id = self.kwargs['pk']
        current_tournament_q = Tournament.objects.filter(pk = tournament_id)
        if not current_tournament_q.exists():
            return redirect("tournaments:tournaments")
        current_tournament = current_tournament_q.first()

        if not current_tournament.approved_by_admin:
            return http.HttpResponseForbidden('The tournament has not yet been approved by the administrator.')

        if Team.objects.filter(tournament = current_tournament).count() < current_tournament.teams_number:

            # TODO check if owner exist in other teams of this tour
            player_q = Player.objects.filter(user = self.request.user)
            if not player_q.exists():
                return redirect("tournaments:tournaments")
            player = player_q.first()

            if (Player.objects.filter(teams__tournament = current_tournament).contains(player)):
                return http.HttpResponseForbidden('Player already has a team.')


            form.instance.owner = self.request.user
            form.instance.tournament = current_tournament
            super().form_valid(form)
            player.teams.add(self.object.id)
            return super().form_valid(form)
            
        else:
            return http.HttpResponseForbidden('Team limit exceeded.')

    def get_success_url(self):
            return reverse("tournaments:detail", kwargs={'tournament_id': self.kwargs['pk']})

# Max Koval (xkoval20)
class TeamsDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = 'teams/team_confirm_delete.html'
    success_url = '/tournaments'

    def form_valid(self, form):
        team_q = Team.objects.filter(pk = self.kwargs['pk'])
        if not team_q.exists():
            return redirect("tournaments:tournaments")
        team = team_q.first()

        owner = team.owner
        if owner == self.request.user or self.request.user.is_superuser:
            success_url = self.get_success_url()
            self.object.delete()
            return http.HttpResponseRedirect(self.success_url)
        else:
            return http.HttpResponseForbidden('no permissions!')

