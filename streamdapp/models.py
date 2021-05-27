from django.db import models

# Create your models here.
class Stream(models.Model):

    stream_name = models.CharField(max_length=250)
    username = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    stream_key = models.CharField(max_length=250)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.stream_name + " - " + self.username
