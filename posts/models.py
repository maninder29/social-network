from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
import os


def media_upload(instance, filename):
    return '{0}/{1}'.format(instance.user.username, filename)


class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.FileField(upload_to=media_upload, null=True, blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id": self.id})

    def extension(self):
        name, extension = os.path.splitext(self.media.name)
        return extension[1:]

    class Meta:
        ordering = ["-timestamp","-updated"]

