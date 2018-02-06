from django.contrib import admin
from .models import User

#add database tables to admin user area here
admin.site.register(User)
