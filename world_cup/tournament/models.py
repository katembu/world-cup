from django.db import models
from django.contrib.auth.models import User


class Countries(models.Model):
    name = models.CharField(max_length=255)
    group = models.CharField(max_length=1)
    position = models.IntegerField()

    class Meta:
        verbose_name = 'Countries'
        verbose_name_plural = 'Countries'


class TournamentGroups(models.Model):
    user = models.ForeignKey(User)
    country = models.ForeignKey(Countries)
    position = models.IntegerField()


class Matches(models.Model):
    home_team = models.ForeignKey(Countries, related_name='home_team')
    away_away = models.ForeignKey(Countries, related_name='away_team')
    winner = models.ForeignKey(Countries, related_name='winner')
    round = models.IntegerField()
    match_number = models.IntegerField()

