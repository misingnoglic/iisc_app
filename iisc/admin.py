from django.contrib import admin
from .models import Event, Professor, Lab


admin.site.register(Event)
admin.site.register(Professor)
admin.site.register(Lab)

# Register your models here.
