from django.urls import path, include
from . import views
from tournaments.views import TournamentsCreateView, TournamentsDeleteView
# from tournaments.views import BracketView

app_name = 'tournaments'

urlpatterns = [

    path('', views.tournaments, name='tournaments'),
    path('detail/<int:tournament_id>', views.detail, name='detail'),
    path('edit/<int:match_id>', views.edit, name='edit'),
    path('bracket/<int:tournament_id>', views.bracket, name='bracket'),
    path('create/', TournamentsCreateView.as_view(), name='create'),
    path('detail/<pk>/delete/', TournamentsDeleteView.as_view(), name='delete'),
    path('leaderdoard/', views.leaderdoard, name='leaderdoard'),

]