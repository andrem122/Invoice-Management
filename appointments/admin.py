from django.contrib import admin
from .models import Appointment

#add database tables to admin user area here
admin.site.register(Appointment)
