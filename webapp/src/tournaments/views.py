import math
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from main.models import Tournament, Team, Round, Match, Player
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.http import JsonResponse
from django.views.generic import View, TemplateView
from django import http
from .forms import CreateRoundForm, create_match_form, ApproveTournamentForm
from django.contrib.auth.decorators import login_required
from rest_framework import status
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.forms import formset_factory, modelformset_factory
from django.contrib import messages
# Create your views here.

def tournaments(request):
    tournament_list = Tournament.objects.all()
    context = {
        'tournament_list': tournament_list,
    }
    return render(request, 'tournaments/tournaments.html', context)

def bracket(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    # team_list = list(Team.objects.filter(tournament=tournament).values())
    team_list = Team.objects.filter(tournament=tournament)
    data_team = serialize("json", team_list)
    data_tournament = serialize("json", [tournament])
    return render(request, 'tournaments/bracket.html', {'team_list': data_team, 'tournament': data_tournament})

# def is_ajax(request):
#     return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
# class BracketView(View):
#     def get(self, request, *args, **kwargs):
#         tournament = Tournament.objects.get(pk=self.kwargs['pk'])
#         team_list = Team.objects.filter(tournament=tournament)
#         data_team = serialize("json", team_list)
#         data_tournament = serialize("json", [tournament])
#         text = request.GET.get('text_t')
#         if is_ajax(request=request):
#             return JsonResponse({'tournament': data_tournament}, status=200)
#         return render(request, 'tournaments/bracket.html', {'team_list': data_team, 'tournament': data_tournament})

def detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    team_list = Team.objects.filter(tournament=tournament)
    round_list = Round.objects.filter(tournament=tournament)

    print(round_list)
    return render(request, 'tournaments/detail.html', {'tournament': tournament, 'team_list': team_list, 'round_list': round_list})


@login_required
def create_round(request, tournament_id):

    tournament = Tournament.objects.get(id = tournament_id)
    round_form = CreateRoundForm(tournament=tournament)
    if request.method == "POST":
        round_form = CreateRoundForm(data = request.POST, tournament=tournament)

        if round_form.is_valid():
            round_form.save()
        else:
            return render(request, 'tournaments/create_round.html', {'round_form': round_form})

        return redirect("tournaments:detail", tournament_id=tournament_id)
    else:
        return render(request, 'tournaments/create_round.html', {'round_form': round_form})


def generate_matches(request, round_id):
    round = Round.objects.get(id = round_id)
    tournament = round.tournament
    teams_list = Team.objects.filter(tournament = tournament)
    MatchForm = create_match_form(teams_list, round)
    MatchFormSet = modelformset_factory(Match, form=MatchForm)

    if request.method == "POST":
        match_formset = MatchFormSet(request.POST)
        if match_formset.is_valid():
            match_formset.save()
        else:
            return render(request, 'tournaments/generate_matches.html', {'match_formset': match_formset})

        return redirect("tournaments:detail", tournament_id=tournament.id)
    else:
        match_formset = MatchFormSet()
        return render(request, 'tournaments/generate_matches.html', {'match_formset': match_formset})
 
def check_form_data(request, matches_formset, teams_list):
    teams_list = list(teams_list)

    if matches_formset.cleaned_data:
        data = matches_formset.cleaned_data
    else:
        messages.error(request, "Unsuccessful operation. Please, setup all team matches.")
        return False

    index = 0
    for item in data:
        if data[index]:

            blue = data[index]['blue']
            if blue in teams_list:
                teams_list.remove(blue)

            red = data[index]['red']
            if red in teams_list:
                teams_list.remove(red)
            index += 1
        else:
            messages.error(request, "Unsuccessful operation. Please, setup all team matches.")
            return False
    if teams_list:
        messages.error(request, "Unsuccessful operation. One of teams has two matches.")
        return False
        
    return True

def approve(request, tournament_id):

    tournament = Tournament.objects.get(id = tournament_id)
    

    if request.method == "POST":
        
        approve_form = ApproveTournamentForm(instance=tournament, data=request.POST)
        if request.user.is_superuser:
            approve_form.save()
            return redirect("tournaments:detail", tournament_id=tournament_id)
        else:
            messages.error(request, "You dont admin privileges.")

        return render(request, 'tournaments/approve_tournament.html', {'approve_form': approve_form})

    else:
        approve_form = ApproveTournamentForm(instance=tournament)
        return render(request, 'tournaments/approve_tournament.html', {'approve_form': approve_form})

    pass

def edit(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    return render(request, 'tournaments/edit.html', {'match': match})

def leaderdoard(request):
    players = Player.objects.all()
    return render(request, 'tournaments/leaderboard.html', {'players': players})

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

