# todo/todo_api/urls.py : API urls.py
from django.urls import path, include
from .views import (
    TournamentListApiView,
    TournamentDetailApiView,
)

urlpatterns = [
    path('api/', TournamentListApiView.as_view()),
    path('api/<int:tournament_id>/', TournamentDetailApiView.as_view()),
]