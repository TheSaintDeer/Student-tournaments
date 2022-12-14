import datetime
from email.policy import default
from pickletools import optimize
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.utils.timezone import datetime
from django.core.validators import MinValueValidator

# Create your models here

class Tournament(models.Model):
    name = models.TextField(max_length=100, help_text='Enter tournament name')
    description = models.TextField(max_length=200, help_text='Enter tournament description')
    logo = models.ImageField(default='default_logos/tournament_default.png', upload_to='tournaments_logo')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    teams_number = models.IntegerField(default=2, validators=[MinValueValidator(2)])
    players_in_team = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    approved_by_admin = models.BooleanField(default=False)
    bracket_exists = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    date_of_start = models.DateTimeField(default=datetime.now())
    pass

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):  # new
        return reverse('detail', args=[str(self.id)])


class Team(models.Model):
    name = models.TextField(max_length=100, help_text='Enter team name')
    logo = models.ImageField(default='default_logos/team_default.png', upload_to='team_logo')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    selected = models.BooleanField(default=False)
    pass

    def __str__(self) -> str:
        return self.name

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team, blank=True)
    bio = models.TextField(max_length=100, help_text='Your bio', blank=True, null=True)
    avatar = models.ImageField(default='default_logos/player_default.png', upload_to='players_avatar', blank=True)
    points = models.IntegerField(default=0)
    wins_matches = models.IntegerField(default=0)
    wins_tournament = models.IntegerField(default=0)
    pass

    def __str__(self) -> str:
        return self.user.username

class Round(models.Model):
    number = models.IntegerField(default=1)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    reward_points = models.IntegerField(default=10)

    def __str__(self) -> str:
        return f'Round: {self.number}'

class Match(models.Model):
    blue = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='blue', null=True, blank=True)
    red = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='red', null=True, blank=True)
    blue_score = models.IntegerField(default=0)
    red_score = models.IntegerField(default=0)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.blue} vs {self.red}'