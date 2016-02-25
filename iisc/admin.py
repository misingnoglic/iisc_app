from django.contrib import admin
from .models import Event, Professor, Lab, FidType


admin.site.register(Event)
admin.site.register(Professor)
admin.site.register(Lab)

@admin.register(FidType)
class FidTypeAdmin(admin.ModelAdmin):
    list_display = ('fiducial_number', 'model_type')


