# Generated by Django 4.1.3 on 2022-11-28 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_player_wins_matches_player_wins_tournament'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
