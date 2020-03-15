from django.contrib import admin
from .models import Appointment_Base, Appointment_Medical, Appointment_Real_Estate

#add database tables to admin user area here
admin.site.register(Appointment_Base)
admin.site.register(Appointment_Medical)
admin.site.register(Appointment_Real_Estate)
