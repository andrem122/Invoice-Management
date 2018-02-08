from django.contrib import admin
from .models import House, Job, Current_Worker

#add database tables to admin user area here
admin.site.register(House)
admin.site.register(Current_Worker)
admin.site.register(Job)
