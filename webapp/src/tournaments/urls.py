from django.urls import path, include
from . import views

app_name = 'tournaments'

urlpatterns = [

    path('', views.tournaments, name='tournaments'),
    path('detail/<int:tournament_id>', views.detail, name='detail'),

]
