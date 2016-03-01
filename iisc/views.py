from .models import Professor, FidType, Rating, Participant
from rest_framework import viewsets
from .serializers import ProfessorSerializer
from django.core import serializers
from django.http import HttpResponse
from django.apps import apps
import json


class ProfessorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Professor.objects.all().order_by('fiducial_number')
    serializer_class = ProfessorSerializer

def ProfessorRaw(request, fn):
    data = serializers.serialize("json",Professor.objects.filter(fiducial_number=fn))
    return HttpResponse(data, content_type="application/json")


def GetObjectFromFiducial(request, fn):
    #import pdb;pdb.set_trace()
    obj_name = FidType.objects.get(fiducial_number=fn).model_type
    Model = apps.get_model(app_label="iisc", model_name=obj_name)
    obj = Model.objects.filter(fiducial_number=fn)
    data = serializers.serialize("json",obj)
    j = json.loads(data)
    j[0]["rating"] = obj[0].rating()
    data = json.dumps(j)
    return HttpResponse(data, content_type="application/json")

def rate(request,email,fn,rating):
    try:
        r = Rating.objects.get(person__email=email, fiducial__fiducial_number=fn)
        r.rating = rating
        r.save()

    except Rating.DoesNotExist:
        r = Rating.objects.create(person = Participant.objects.get(email=email),
                                  fiducial = FidType.objects.get(fiducial_number=fn),
                                  rating = rating)
        r.save()
    return HttpResponse(json.dumps({'success':'True'}), content_type="application/json")

def register(request,email,name):
    if Participant.objects.filter(email=email).count() > 0:
        #return HttpResponse(json.dumps({'success':'False', 'error':'Already Exists'}), content_type="application/json")
        pass
    else:
        p = Participant.objects.create(email=email, name=name)
        p.save()
    return HttpResponse(json.dumps({'success':'True'}), content_type="application/json")