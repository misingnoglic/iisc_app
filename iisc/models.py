from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    name = models.CharField(max_length=20)
    time = models.TimeField()
    fiducial_number = models.IntegerField()
    description = models.TextField()
    votes = models.IntegerField()


class Professor(models.Model):
    name = models.CharField(max_length=20)
    research_field = models.CharField(max_length=30)
    room = models.IntegerField()
    fiducial_number = models.IntegerField()
    description = models.TextField()

    def __unicode__(self):
        return self.name

class Lab(models.Model):
    pi = models.ForeignKey(Professor)
    room = models.IntegerField()
    name = models.CharField(max_length=20)
    fiducial_number = models.IntegerField()
    description = models.TextField()

#class Participant(models.Model):
