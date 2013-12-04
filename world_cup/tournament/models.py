from django.db import models
from django.contrib.auth.models import User


class Countries(models.Model):
    name = models.CharField(max_length=255)
    group = models.CharField(max_length=1)
    position = models.IntegerField()
    final_position = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Countries'
        verbose_name_plural = 'Countries'


class Brackets(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        try:
            Brackets.objects.get(user=self.user, name=self.name)
            return
        except:
            super(Brackets, self).save(*args, **kwargs)


class GroupPredictions(models.Model):
    bracket = models.ForeignKey(Brackets)
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


class MatchPredictions(models.Model):
    bracket = models.ForeignKey(Brackets)
    home_team = models.ForeignKey(Countries, related_name='home_team_coice', null=True)
    home_score = models.IntegerField(null=True)
    away_team = models.ForeignKey(Countries, related_name='away_team_choice', null=True)
    away_score = models.IntegerField(null=True)
    winner = models.ForeignKey(Countries, related_name='winner_choice', null=True)
    round = models.IntegerField()
    match_number = models.IntegerField()
