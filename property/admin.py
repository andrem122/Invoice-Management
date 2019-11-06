from django.contrib import admin
from .models import Property

#add database tables to admin user area here
admin.site.register(Property)
