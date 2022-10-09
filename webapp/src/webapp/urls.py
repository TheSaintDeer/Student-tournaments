from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, serializers, viewsets

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('', include('main.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('api.urls')),
    path('tournaments/', include('tournaments.urls')),
    path('teams/', include('teams.urls')),

]