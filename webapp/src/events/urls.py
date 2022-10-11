from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('events/', views.index, name='events'),
    path('detail/<int:tournament_id>', views.detail, name='detail'),
    path('create_event/', views.create, name='create_event')
]
