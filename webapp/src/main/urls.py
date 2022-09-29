from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('news', views.news),
    path('tournaments', views.tournaments),
    path('freepage', views.freepage),
    path('login', views.login),
    path('notification', views.notification)
]