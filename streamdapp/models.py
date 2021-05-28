from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Stream(models.Model):

    stream_name = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    description = models.TextField(max_length=1000)
    stream_key = models.CharField(max_length=250)
    stream_url = models.CharField(max_length=250, default="")
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.stream_name