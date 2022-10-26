from urllib import request
from django.shortcuts import render, get_object_or_404
from main.models import Team, Player, Tournament
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import http

# Create your views here.
def detail(request, team_id):
    current_team = get_object_or_404(Team, pk=team_id)
    players_list = Player.objects.filter(teams__id = team_id)
    return render(request, 'teams/detail.html', {'team': current_team, 'players_list': players_list})

class TeamsCreateView(LoginRequiredMixin, CreateView):
    model = Team
    template_name = 'teams/team_create_form.html'
    fields = ['name', 'logo']
    success_url = '/tournaments'



    def form_valid(self, form):
        current_tournament = Tournament.objects.get(pk = self.kwargs['pk'])
        
        if Team.objects.filter(tournament = current_tournament).count() < current_tournament.teams_number:
            form.instance.owner = self.request.user
            form.instance.tournament = current_tournament
            super().form_valid(form)
            Player.objects.get(pk = self.request.user.pk).teams.add(self.object.id)
            return http.HttpResponseRedirect(self.success_url)
        else:
            return http.HttpResponseForbidden('too much teams!')



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

