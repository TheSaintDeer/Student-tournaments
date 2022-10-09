from django.urls import path, include
from . import views

app_name = 'teams'

urlpatterns = [

    path('detail/<int:team_id>', views.detail, name='detail'),

]

