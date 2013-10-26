from django.db import models
from django.contrib.auth.models import User


class Countries(models.Model):
    name = models.CharField(max_length=255)
    group = models.CharField(max_length=1)
    position = models.IntegerField()

    class Meta:
        verbose_name = 'Countries'
        verbose_name_plural = 'Countries'


class GroupWinners(models.Model):
    user = models.ForeignKey(User)
    country = models.ForeignKey(Countries)
    position = models.IntegerField()


class Matches(models.Model):
    home_team = models.ForeignKey(Countries, related_name='home_team', null=True)
    home_score = models.IntegerField(null=True)
    away_team = models.ForeignKey(Countries, related_name='away_team', null=True)
    away_score = models.IntegerField(null=True)
    winner = models.ForeignKey(Countries, related_name='winner', null=True)
    round = models.IntegerField()
    match_number = models.IntegerField()

