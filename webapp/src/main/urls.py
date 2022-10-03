from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('tournaments/', views.tournaments, name='tournaments'),
    path('teams/', views.teams, name='teams'),
    path('login/', views.login, name='login'),
    path('notification/', views.notification, name='notification')
]