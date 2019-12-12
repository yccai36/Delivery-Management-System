import datetime

from django.db import models
from django.utils import timezone


class User(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    time = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    pub_time = models.DateTimeField('date published')
    status = models.BooleanField(default=False)
    ## 42.4459932, -76.4856997
    lat = models.FloatField(default=42.4406)
    lng = models.FloatField(default=-76.4966)
    distance = models.FloatField(default=0)

    def __str__(self):
        return self.firstname +" "+ self.lastname
    def was_published_recently(self):
        return self.pub_time >= timezone.now() - datetime.timedelta(days=1)

