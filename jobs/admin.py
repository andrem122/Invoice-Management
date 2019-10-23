from django.contrib import admin
from .models import House, Job, Request_Payment

#add database tables to admin user area here
admin.site.register(House)
admin.site.register(Job)
admin.site.register(Request_Payment)
