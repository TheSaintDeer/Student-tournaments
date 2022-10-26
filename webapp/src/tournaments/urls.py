from django.urls import path, include
from . import views
from tournaments.views import TournamentsCreateView, TournamentsDeleteView

app_name = 'tournaments'

urlpatterns = [

    path('', views.tournaments, name='tournaments'),
    path('detail/<int:tournament_id>', views.detail, name='detail'),
    path('create/', TournamentsCreateView.as_view(), name='create'),   
    path('detail/<pk>/delete/', TournamentsDeleteView.as_view(), name='delete'),   

]

