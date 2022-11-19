# Generated by Django 4.1.1 on 2022-11-18 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(help_text='Enter tournament name', max_length=100)),
                ('description', models.TextField(help_text='Enter description tournament', max_length=200)),
                ('logo', models.ImageField(default='none', upload_to='')),
                ('count_teams', models.IntegerField()),
                ('count_players_in_team', models.IntegerField()),
                ('reward', models.IntegerField()),
                ('state', models.CharField(choices=[('CM', 'Complete'), ('UN', 'Underway'), ('PN', 'Pending')], default='PN', max_length=2)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(help_text='Enter team name', max_length=100)),
                ('logo', models.ImageField(default='none', upload_to='')),
                ('players', models.ManyToManyField(through='main.Player', to=settings.AUTH_USER_MODEL)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tournament')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='teams',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.team'),
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]