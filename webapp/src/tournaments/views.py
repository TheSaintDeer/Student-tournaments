from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from main.models import Tournament, Team, Round
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import http
from .forms import CreateRoundForm
from django.contrib.auth.decorators import login_required
from rest_framework import status
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

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
    round_list = Round.objects.filter(tournament=tournament)
    print(round_list)
    return render(request, 'tournaments/detail.html', {'tournament': tournament, 'team_list': team_list, 'round_list': round_list})


@login_required
@csrf_exempt
def create_round(request):
    if request.method == 'POST':
        

        print(request.POST)
        tournament = Tournament.objects.get(id = request.POST['tournament_id'])
        round = Round.objects.create(tournament = tournament)
        round.save()
        
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

