from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class FidType(models.Model):
    fiducial_number = models.IntegerField()
    model_type = models.CharField(max_length=50)

class FiducialObject(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        #import pdb ; pdb.set_trace()
        record = FidType(fiducial_number=self.fiducial_number, model_type=self._meta.object_name)
        record.save()
        super(FiducialObject, self).save(*args, **kwargs)  # Call the "real" save() method.



class Event(FiducialObject):
    name = models.CharField(max_length=20)
    time = models.TimeField()
    fiducial_number = models.IntegerField()
    description = models.TextField()
    votes = models.IntegerField()


class Professor(FiducialObject):
    name = models.CharField(max_length=20)
    research_field = models.CharField(max_length=30)
    room = models.IntegerField()
    fiducial_number = models.IntegerField()
    description = models.TextField()


    def __unicode__(self):
        return self.name


class Lab(FiducialObject):
    pi = models.ForeignKey(Professor)
    room = models.IntegerField()
    name = models.CharField(max_length=20)
    fiducial_number = models.IntegerField()
    description = models.TextField()

#class Participant(models.Model):
