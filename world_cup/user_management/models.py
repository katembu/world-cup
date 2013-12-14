from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    language = models.CharField(max_length=255, blank=True)
    newsletter = models.BooleanField(default=False)
