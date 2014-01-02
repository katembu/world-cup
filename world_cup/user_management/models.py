from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from tournament.models import CompetitiveGroups


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    language = models.CharField(max_length=255, blank=True)
    newsletter = models.BooleanField(default=False)
    message_notifications = models.BooleanField(default=True)  # Receive email when you receive a message
    searchable = models.BooleanField(default=True)  # Searchable throughout the site
    show_full_name = models.BooleanField(default=False)  # Show full name on site

    def resize_image(self):
        from PIL import Image
        from cStringIO import StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        THUMBNAIL_SIZE = (128, 128)

        image = Image.open(StringIO(self.image.read()))
        image_type = image.format.lower()
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        temp_handle = StringIO()
        image.save(temp_handle, image_type)
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], temp_handle.read(),
                                 content_type='image/%s' % image_type)

        self.image.save('%s.%s' % (os.path.splitext(suf.name)[0], image_type), suf, save=False)

    def save(self, **kwargs):
        if self.image and not (self.image.width == 128 or self.image.height == 128):
            self.resize_image()
        super(CustomUser, self).save()


class UserMessages(models.Model):
    to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_to')
    sent_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_by')
    date_sent = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    read = models.BooleanField(default=False)
    group = models.ForeignKey(CompetitiveGroups, null=True, blank=True)
    reply_to = models.ForeignKey('user_management.UserMessages', null=True, blank=True)
