from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


# Create your models here.

# Model that stores stream information
class Stream(models.Model):
    # The stream title
    stream_name = models.CharField("stream name", max_length=100)

    # The author of this stream
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="author", on_delete=models.CASCADE, default=1)

    # The stream description
    description = models.TextField("description", max_length=1000)

    # The stream key used by the author to stream through rtmp
    stream_key = models.CharField("stream key", max_length=100)

    # The hls stream key where people can watch the stream
    # http://0.0.0.0/live/{hls_key}/index.m3u8
    hls_key = models.CharField("stream url", max_length=100, default="")

    # The amount of likes of this stream
    likes = models.IntegerField("likes", default=0)

    # Is the author streaming?
    is_streaming = models.BooleanField("is streaming", default=False)

    def __str__(self):
        return self.stream_name
