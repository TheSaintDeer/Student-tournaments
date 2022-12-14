from django.urls import path, include
from . import views
from tournaments.views import TournamentsCreateView, TournamentsDeleteView

app_name = 'tournaments'

urlpatterns = [

    path('', views.tournaments, name='tournaments'),
    path('detail/<int:tournament_id>', views.detail, name='detail'),
    path('edit/<int:match_id>', views.edit, name='edit'),
    path('bracket/<int:tournament_id>', views.bracket, name='bracket'),
    path('create/', TournamentsCreateView.as_view(), name='create'),
    path('detail/<pk>/delete/', TournamentsDeleteView.as_view(), name='delete'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('approve/<int:tournament_id>', views.approve, name='approve'),
    path('create_round/<int:tournament_id>', views.create_round, name='create_round'),
    path('create_tournament/', views.create_tournament, name='create_tournament'),
    path('tournaments_list/', views.tournaments_list, name='tournaments_list'),

# generate_matches
]