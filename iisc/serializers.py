from .models import Professor
from rest_framework import serializers


class ProfessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professor
        fields = ('name', 'research_field', 'room', 'fiducial_number', 'description')
