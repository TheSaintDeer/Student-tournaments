# Generated by Django 4.1.2 on 2022-11-29 01:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_tournament_date_of_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='date_of_start',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 29, 1, 6, 4, 26366)),
        ),
    ]