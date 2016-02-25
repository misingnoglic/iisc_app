from .models import Professor, FidType
from rest_framework import viewsets
from .serializers import ProfessorSerializer
from django.core import serializers
from django.http import HttpResponse
from django.apps import apps


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
    return HttpResponse(data, content_type="application/json")