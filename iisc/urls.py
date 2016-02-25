__author__ = 'arya'
from django.conf.urls import patterns, url
from iisc import views


urlpatterns = patterns('',
    url(r'^profs/(\d+)/$', views.ProfessorRaw, name='register'),
    url(r'^fn/(\d+)/$', views.GetObjectFromFiducial, name='fn')
)