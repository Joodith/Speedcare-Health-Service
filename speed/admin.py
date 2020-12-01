from django.contrib import admin
from speed.models import Clinic,Doctor,User,MapDetail,TimeSlot

# Register your models here.
admin.site.register(Clinic)
admin.site.register(Doctor)
admin.site.register(MapDetail)
admin.site.register(TimeSlot)

