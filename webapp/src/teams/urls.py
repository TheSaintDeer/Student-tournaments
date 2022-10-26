from django.urls import path, include
from . import views
from teams.views import TeamsCreateView, TeamsDeleteView

app_name = 'teams'

urlpatterns = [

    path('detail/<int:team_id>', views.detail, name='detail'),
    path('create/<pk>', TeamsCreateView.as_view(), name='create'),   
    path('detail/<pk>/delete/', TeamsDeleteView.as_view(), name='delete'), 

]

