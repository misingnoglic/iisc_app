from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class FidType(models.Model):
    fiducial_number = models.IntegerField(unique=True)
    model_type = models.CharField(max_length=50)

class FiducialObject(models.Model):

    fiducial_number = models.IntegerField(unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # If it's being created for the first time - check to make sure the fn doesn't exist
        # If it's being updated - If the fn is the same don't worry, else:
            # Make sure the new fn doesn't exist, but otherwise update the old FidType

        Model = apps.get_model(app_label="iisc", model_name=self._meta.object_name)
        duplicate_fn_error = ValidationError(
                    _('Already Existing Fiducial Number: %s' % self.fiducial_number),
                    code='existingfn',
                    params={'fiducial_number': self.fiducial_number})

        if self.pk:
            old_fn = Model.objects.get(pk=self.pk).fiducial_number  # The old fn from the database
        else:
            old_fn = self.fiducial_number

        # If this fn already exists, throw an error
        if self.pk and FidType.objects.filter(fiducial_number=self.fiducial_number):
            if old_fn != self.fiducial_number:
                raise duplicate_fn_error

        if not self.pk: # If it is created for the first time - save the record
            record = FidType(fiducial_number=self.fiducial_number, model_type=self._meta.object_name)
            record.save()
        else:
            if old_fn != self.fiducial_number:  # If the fn is updated
                f = FidType.objects.get(fiducial_number=old_fn)  # update the number in the FidType object & save
                f.fiducial_number = self.fiducial_number
                f.save()
            else:  # If the fn didn't update in the update, then don't do anything
                pass

        super(FiducialObject, self).save(*args, **kwargs)  # Call the "real" save() method.


class Event(FiducialObject):
    name = models.CharField(max_length=20)
    time = models.TimeField()
    description = models.TextField()
    votes = models.IntegerField()


class Professor(FiducialObject):
    name = models.CharField(max_length=20)
    research_field = models.CharField(max_length=30)
    room = models.IntegerField()
    description = models.TextField()


    def __unicode__(self):
        return self.name


class Lab(FiducialObject):
    pi = models.ForeignKey(Professor)
    room = models.IntegerField()
    name = models.CharField(max_length=20)
    description = models.TextField()
    faculty_photo = models.ImageField(upload_to="media/", blank=True)
    video = models.FileField(upload_to="media/", blank=True)

    def __unicode__(self):
        return self.name

#class Participant(models.Model):
