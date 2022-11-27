from django.contrib import admin
from main.models import Tournament, Team, Player, Match, Round

admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Round)