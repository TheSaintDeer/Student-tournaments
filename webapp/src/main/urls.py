from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login, name='login'),
    path('notification/', views.notification, name='notification'),
    path('profile/', views.profile, name='profile'),
    path("registration/", views.registration_request, name="registration"),
    path("create_post/", views.create_post, name="create_post"),
    path("update_profile/", views.update_profile, name="update_profile"),


]