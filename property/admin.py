from django.contrib import admin
from .models import Company, Company_Disabled_Days, Company_Disabled_Datetimes

#add database tables to admin user area here
admin.site.register(Company)
admin.site.register(Company_Disabled_Days)
admin.site.register(Company_Disabled_Datetimes)
