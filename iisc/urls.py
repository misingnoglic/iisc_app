__author__ = 'arya'
from django.conf.urls import patterns, url
from iisc import views


urlpatterns = patterns('',
    #url(r'^profs/(\d+)/$', views.ProfessorRaw, name='register'),
    url(r'^fn/(\d+)/$', views.GetObjectFromFiducial, name='fn'),
    url(r'^fn/(?P<fn>\d+)/rate/(?P<user_id>\d+)/(?P<rating>\d+)$', views.rate, name='rate'),
    url(r'^register/$', views.register, name='register'),
    url(r'^fn/(?P<fn>\d+)/save/(?P<user_id>\d+)/$', views.save_fid, name='save'),
)