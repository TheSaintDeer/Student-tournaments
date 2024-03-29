import math
import json

from main.models import Tournament, Team, Round, Match, Player
from .forms import CreateRoundForm, create_match_form, ApproveTournamentForm, CreateTournamentForm

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, DeleteView
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.serializers import serialize
from django import http
from django.forms import formset_factory, modelformset_factory
from rest_framework import status

def tournaments_list(request):

    tournament_list = reversed(Tournament.objects.all().order_by('date_of_start'))
    context = {
        'tournament_list': tournament_list,
    }
    return render(request, 'tournaments/tournament_list.html', context)

def tournaments(request):

    create_tour_form = CreateTournamentForm();


    tournament_list = reversed(Tournament.objects.all().order_by('date_of_start'))
    context = {
        'tournament_list': tournament_list,
        'create_tour_form': create_tour_form,
    }
    return render(request, 'tournaments/tournaments.html', context)


@login_required
@csrf_protect
def create_tournament(request):

    if request.method == 'POST':

        print(request.POST)

        create_tour_form = CreateTournamentForm(request.POST)

        if create_tour_form.is_valid():
            instance = create_tour_form.save(commit=False)
            instance.owner = request.user
            instance.save()

            data = {'result': 'success'}
            return JsonResponse(
                data=data,
                safe=False,
                content_type="application/json",
                status=status.HTTP_200_OK
            )

    return JsonResponse(
            data=None,
            safe=False,
            content_type="application/json",
            status=status.HTTP_200_OK
    )
    pass

def bracket(request, tournament_id, winner=None, top_team=None):
    tournament_q = Tournament.objects.filter(id=tournament_id)
    if not tournament_q.exists():
        return redirect("tournaments:tournaments")
    tournament = tournament_q.first()

    team_list = Team.objects.filter(tournament=tournament)
    rounds = Round.objects.all()
    matches = Match.objects.all()
    req_rounds = Round.objects.filter(tournament=tournament)
    players = Player.objects.all()
    tournament_finished = True
    aux = ''
    if is_ajax(request):
        aux = request.GET.get('result_button')
    if request.method == 'GET' and aux == 'pressed':
        print("Result button pressed")
        owner = tournament.owner
        if owner != request.user and not request.user.is_superuser:
            return http.JsonResponse({'result': 'forbidden'})
        # Check if all matches are correct when pressed result button
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
        # Picks winners of previous round's matches
        for round in req_rounds:
            if not round.finished:
                prev_round_q = Round.objects.filter(tournament=tournament, number=round.number-1)
                if not prev_round_q.exists():
                    return redirect("tournaments:tournaments")
                prev_round = prev_round_q.first()

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
                    for player in players:
                        teams_of_player = player.teams.all()
                        for team in teams_of_player:
                            if team == curr_match.blue or team == curr_match.red:
                                player.wins_matches += 1
                                player.save()
                    curr_match.save()
                    k += 2
                break
        # If all rounds are finished give the winner statistic point
        for round in req_rounds:
            if not round.finished:
                tournament_finished = False
        if tournament_finished and not tournament.finished:
            for round in req_rounds:
                if len(req_rounds) == round.number:
                    for match in matches:
                        if match.round == round:
                            if match.blue_score > match.red_score:
                                top_team = match.blue
                            else:
                                top_team = match.red
            for player in players:
                teams_of_player = player.teams.all()
                for team in teams_of_player:
                    if team == top_team:
                        player.wins_tournament += 1
                        player.wins_matches += 1
                        player.save()
            tournament.finished = True
            tournament.save()
        return http.JsonResponse({'result': 'success'})

    if request.method == 'GET' and is_ajax(request) and aux != 'pressed':
        owner = tournament.owner
        if owner != request.user and not request.user.is_superuser:
            return http.JsonResponse({'result': 'forbidden'})
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

# Max Koval (xkoval20)
def detail(request, tournament_id):
    tournament_q = Tournament.objects.filter(id=tournament_id)
    if not tournament_q.exists():
        return redirect("tournaments:tournaments")
    tournament = tournament_q.first()

    team_list = Team.objects.filter(tournament=tournament)
    round_list = Round.objects.filter(tournament=tournament)

    print(round_list)
    return render(request, 'tournaments/detail.html', {'tournament': tournament, 'team_list': team_list, 'round_list': round_list})


# Max Koval (xkoval20)
@login_required
def create_round(request, tournament_id):

    tournament_q = Tournament.objects.filter(id=tournament_id)
    if not tournament_q.exists():
        return redirect("tournaments:tournaments")
    tournament = tournament_q.first()
    
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

# Max Koval (xkoval20)
def approve(request, tournament_id):

    tournament_q = Tournament.objects.filter(id = tournament_id)
    if not tournament_q.exists():
        return redirect("tournaments:tournaments")
    tournament = tournament_q.first()

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

# Anvar Kilybayev (xkilyb00)
def edit(request, match_id):
    match_q = Match.objects.filter(pk=match_id)
    if not match_q.exists():
        return redirect("tournaments:tournaments")
    match = match_q.first()

    team_list = Team.objects.filter(tournament=match.round.tournament)
    owner = match.round.tournament.owner
    if owner != request.user and not request.user.is_superuser:
        return http.HttpResponseForbidden('permission denied!')

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
            blue_q = Team.objects.filter(name=blue_team, tournament=match.round.tournament)
            red_q = Team.objects.filter(name=red_team, tournament=match.round.tournament)
            if not blue_q.exists() or not red_q.exists():
                return redirect("tournaments:tournaments")
            blue = blue_q.first()
            red = red_q.first()

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

# Max Koval (xkoval20)
def leaderboard(request):
    players = Player.objects.all()
    return render(request, 'tournaments/leaderboard.html', {'players': players})

# Max Koval (xkoval20)
class TournamentsCreateView(LoginRequiredMixin, CreateView):
    model = Tournament
    fields = ['name', 'description', 'logo', 'teams_number', 'players_in_team', 'date_of_start']
    template_name = 'tournaments/tournament_create_form.html'
    success_url = '/tournaments'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

# Max Koval (xkoval20)
class TournamentsDeleteView(LoginRequiredMixin, DeleteView):
    model = Tournament
    template_name = 'tournaments/tournament_confirm_delete.html'
    success_url = '/tournaments'

    def form_valid(self, form):

        tournament_q = Tournament.objects.filter(pk=self.kwargs['pk'])
        if not tournament_q.exists():
                return redirect("tournaments:tournaments")
        tournament = tournament_q.first()

        owner = tournament.owner
        if owner == self.request.user or self.request.user.is_superuser:
            success_url = self.get_success_url()
            self.object.delete()
            return http.HttpResponseRedirect(success_url)
        else:
            return http.HttpResponseForbidden('no permissions!')

