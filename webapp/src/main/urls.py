from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path("registration/", views.registration_request, name="registration"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path("update_profile_picture/", views.update_profile_picture, name="update_profile_picture"),

    path('user_detail/<int:user_id>', views.user_detail, name='user_detail'), 
]