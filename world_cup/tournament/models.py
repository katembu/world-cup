from django.db import models
from django.conf import settings


class Countries(models.Model):
    name = models.CharField(max_length=255)
    group = models.CharField(max_length=1)
    position = models.IntegerField()
    final_position = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = 'Countries'
        verbose_name_plural = 'Countries'


class Brackets(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        try:
            Brackets.objects.get(user=self.user, name=self.name)
            return
        except:
            super(Brackets, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = 'Bracket'
        verbose_name_plural = 'Brackets'


class GroupPredictions(models.Model):
    bracket = models.ForeignKey(Brackets)
    country = models.ForeignKey(Countries)
    position = models.IntegerField()

    def __unicode__(self):
        return u'%s' % self.country

    class Meta:
        verbose_name = 'Group Prediction'
        verbose_name_plural = 'Group Predictions'


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

    def __unicode__(self):
        return u'%s' % self.winner

    class Meta:
        verbose_name = 'Match Prediction'
        verbose_name_plural = 'Match Predictions'


class CompetitiveGroups(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, blank=True)
    brackets = models.ManyToManyField(Brackets)

    def get_group_emails(self):
        group_emails = []
        for bracket in self.brackets.all():
            group_emails.append(bracket.user.email)
        return group_emails

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = 'Competitive Group'
        verbose_name_plural = 'Competitive Groups'


class GroupPermissions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    group = models.ForeignKey(CompetitiveGroups)
    allowed = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s - %s' % (self.requester, self.group)

    class Meta:
        verbose_name = 'Group Permission'
        verbose_name_plural = 'Group Permissions'
