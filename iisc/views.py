from .models import Professor, FidType, Rating, Participant, FiducialObject, Lab
from rest_framework import viewsets
from .serializers import ProfessorSerializer
from django.core import serializers
from django.http import HttpResponse
from django.apps import apps
import json
from django.views.decorators.csrf import csrf_exempt



class ProfessorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Professor.objects.all().order_by('fiducial_number')
    serializer_class = ProfessorSerializer

def ProfessorRaw(request, fn):
    data = serializers.serialize("json",Professor.objects.filter(fiducial_number=fn))
    return HttpResponse(data, content_type="application/json")


def GetObjectFromFiducial(request, fn, string=False):
    if string:
        fn = FidType.objects.get(name=fn).fiducial_number
    obj_name = FidType.objects.get(fiducial_number=fn).model_type
    Model = apps.get_model(app_label="iisc", model_name=obj_name)
    obj = Model.objects.filter(fiducial_number=fn)
    data = serializers.serialize("json",obj)
    j = json.loads(data)
    j[0]["rating"] = obj[0].rating()
    data = json.dumps(j)
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
def rate(request,user_id,fn,rating, string=False):
    if string:
        try:
            fn = FidType.objects.get(name=fn).fiducial_number
        except:
            e = Lab.objects.create(name=fn, fiducial_number=fn.__hash__(), room=1)
            e.save()
            fn=e.fiducial_number
    try:
        r = Rating.objects.get(person__pk=user_id, fiducial__fiducial_number=fn)
        r.rating = rating
        r.save()

    except Rating.DoesNotExist:
        r = Rating.objects.create(person=Participant.objects.get(pk=user_id),
                                  fiducial=FidType.objects.get(fiducial_number=fn),
                                  rating=rating)
        r.save()
    return HttpResponse(json.dumps({'success':'True', 'total_rating':FidType.objects.get(fiducial_number=fn).rating()}), content_type="application/json")

@csrf_exempt
def register(request):
    if request.method == 'POST':
        email = request.POST["email"]
        name = request.POST["name"]
        if Participant.objects.filter(email=email).count() > 0:
            p = Participant.objects.get(email=email)
            return HttpResponse(json.dumps({'UserID':p.pk,'success':'False', 'error':'Already Exists'}), content_type="application/json")
        else:
            p = Participant.objects.create(email=email, name=name)
            p.save()
        return HttpResponse(json.dumps({'success': 'True','UserID':p.pk}), content_type="application/json")


def save_fid(request,user_id, fn, string=False):
    if string:
        fn = FidType.objects.get(name=fn).fiducial_number
    user = Participant.objects.get(pk=user_id)
    user.saved.add(FidType.objects.get(fiducial_number=fn))
    user.save()
    return HttpResponse(json.dumps({'success': 'True'}), content_type="application/json")
