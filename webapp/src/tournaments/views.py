import math
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from main.models import Tournament, Team, Round, Match, Player
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
import json
from django import http
from .forms import CreateRoundForm, create_match_form, ApproveTournamentForm
from django.contrib.auth.decorators import login_required
from rest_framework import status
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.forms import formset_factory, modelformset_factory
from django.contrib import messages
# Create your views here.

def tournaments(request):
    tournament_list = reversed(Tournament.objects.all())
    context = {
        'tournament_list': tournament_list,
    }
    return render(request, 'tournaments/tournaments.html', context)

def bracket(request, tournament_id, winner=None):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    team_list = Team.objects.filter(tournament=tournament)
    rounds = Round.objects.all()
    matches = Match.objects.all()
    req_rounds = Round.objects.filter(tournament=tournament)
    aux = ''
    if is_ajax(request):
        aux = request.GET.get('result_button')
    if request.method == 'GET' and aux == 'pressed':
        print("Result button pressed")
        for round in req_rounds:
            if not round.finished:
                print("Round number:", round.number)
                req_matches = Match.objects.filter(round=round)
                round.finished = True
                for match in req_matches:
                    print("Match id:", match.id)
                    if match.blue is None and match.red is None:
                        round.finished = False
                        return http.JsonResponse({'result': 'error_none'})
                    elif match.red_score == match.blue_score:
                        round.finished = False
                        return http.JsonResponse({'result': 'error_tie'})
                    match.finished = True
                    match.save()
                round.save()
                break
        for round in req_rounds:
            if not round.finished:
                prev_round = Round.objects.get(tournament=tournament, number=round.number-1)
                print(prev_round.number)
                curr_matches = Match.objects.filter(round=round)
                prev_matches = Match.objects.filter(round=prev_round)
                j = 0
                k = 2
                for curr_match in curr_matches:
                    while j < k:
                        if len(prev_matches) > j:
                            if prev_matches[j].blue_score > prev_matches[j].red_score:
                                winner = prev_matches[j].blue
                            else:
                                winner = prev_matches[j].red
                            if j % 2 == 0:
                                curr_match.blue = winner
                            else:
                                curr_match.red = winner
                        j += 1
                    print(curr_match.blue, curr_match.red)
                    curr_match.save()
                    k += 2
                break

        return http.JsonResponse({'result': 'success'})

    if request.method == 'GET' and is_ajax(request) and aux != 'pressed':
        matches_list = []
        data_from_ajax = json.loads(request.GET.get('bracket_data'))
        tournament.bracket_exists = True
        tournament.save()
        cnt = 1
        for round in data_from_ajax["rounds_list"]:
            new_round = Round(number=cnt, tournament=tournament)
            cnt += 1
            new_round.save()
            for match in round:
                new_match = Match(round=new_round)
                new_match.save()
                matches_list.append(new_match.id)
        rounds = Round.objects.all()
        matches = Match.objects.all()
        return http.JsonResponse({'matches': matches_list}, status=200)
    data_team = serialize("json", team_list)
    data_tournament = serialize("json", [tournament])
    return render(request, 'tournaments/bracket.html', {'team_list': data_team, 'tournament': data_tournament, 't_jinja': tournament, 'round_list': rounds, 'match_list': matches})

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

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
    team_list = Team.objects.filter(tournament=match.round.tournament)
    if all(team.selected is True for team in team_list):
        for team in team_list:
            if match.blue == team or match.red == team:
                team.selected = False
                team.save()
    if request.method == 'POST':
        response_data = {}
        response_data['result'] = 'success'
        blue_team = request.POST['blue_team']
        red_team = request.POST['red_team']
        blue_score = request.POST['blue_score']
        red_score = request.POST['red_score']
        print(blue_team, red_team)
        # if blue_team == red_team:
        #     print("Same team selected")
        #     response_data['result'] = 'error_same'
        if blue_team is None or red_team is None:
            print("One of the team is none")
            response_data['result'] = 'error_none'
        elif blue_team == 'None' or red_team == 'None':
            print("One of the team is none")
            response_data['result'] = 'error_none'
        else:
            print("Teams are different")
            if match.blue is not None and match.red is not None:
                match.blue.selected = False
                match.red.selected = False
                match.blue.save()
                match.red.save()
            # player = Player.objects.get(id=request.user.id)
            blue = Team.objects.get(name=blue_team, tournament=match.round.tournament)
            red = Team.objects.get(name=red_team, tournament=match.round.tournament)
            blue.selected = True
            red.selected = True
            blue.save()
            red.save()
            match.blue = blue
            match.red = red
            match.blue_score = blue_score
            match.red_score = red_score
            match.save()
        return http.HttpResponse(
            json.dumps(response_data),
            content_type="application/json")
    return render(request, 'tournaments/edit.html', {'match': match, 'team_list': team_list})

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

