from .models import Professor
from rest_framework import viewsets
from .serializers import ProfessorSerializer
from django.core import serializers
from django.http import HttpResponse


class ProfessorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Professor.objects.all().order_by('fiducial_number')
    serializer_class = ProfessorSerializer

def ProfessorRaw(request, fn):
    data = serializers.serialize("json",Professor.objects.filter(fiducial_number=fn))
    return HttpResponse(data, content_type="application/json")