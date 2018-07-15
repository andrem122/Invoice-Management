from django.contrib import admin
from .models import Expenses

#add database tables to admin user area here
admin.site.register(Expenses)
