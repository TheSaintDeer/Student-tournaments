from django.shortcuts import render, get_object_or_404
from main.models import Tournament, Team, Round
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import http


# Create your views here.

def tournaments(request):
    tournament_list = Tournament.objects.all()
    context = {
        'tournament_list': tournament_list,
    }
    return render(request, 'tournaments/tournaments.html', context)


def detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    team_list = Team.objects.filter(tournament=tournament)
    return render(request, 'tournaments/detail.html', {'tournament': tournament, 'team_list': team_list})


class TournamentsCreateView(LoginRequiredMixin, CreateView):
    model = Tournament
    template_name = 'tournaments/tournament_create_form.html'
    fields = ['name', 'description', 'logo', 'teams_number', 'players_in_team']
    success_url = '/tournaments'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TournamentsDeleteView(LoginRequiredMixin, DeleteView):
    model = Tournament
    template_name = 'tournaments/tournament_confirm_delete.html'
    success_url = '/tournaments'

    def form_valid(self, form):
        owner = Tournament.objects.get(pk=self.kwargs['pk']).owner
        if owner == self.request.user:
            success_url = self.get_success_url()
            self.object.delete()
            return http.HttpResponseRedirect(success_url)
        else:
            return http.HttpResponseForbidden('no permissions!')


class RoundCreateView(LoginRequiredMixin, CreateView):
    model = Round
    template_name = 'tournaments/tournament_create_form.html'
    fields = ['name', 'description', 'logo']
    success_url = '/tournaments'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)