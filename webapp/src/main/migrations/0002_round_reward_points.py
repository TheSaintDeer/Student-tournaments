# Generated by Django 4.1.2 on 2022-11-26 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='reward_points',
            field=models.IntegerField(default=10),
        ),
    ]
