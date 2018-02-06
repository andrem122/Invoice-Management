from django.contrib import admin
from .models import House, Job

#add database tables to admin user area here
admin.site.register(House)
admin.site.register(Job)
