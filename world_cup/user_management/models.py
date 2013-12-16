from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from tournament.models import CompetitiveGroups


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    language = models.CharField(max_length=255, blank=True)
    newsletter = models.BooleanField(default=False)


class UserMessages(models.Model):
    to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_to')
    sent_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_by')
    date_sent = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    read = models.BooleanField(default=False)
    group = models.ForeignKey(CompetitiveGroups, null=True, blank=True)
    reply_to = models.ForeignKey('user_management.UserMessages', null=True, blank=True)
