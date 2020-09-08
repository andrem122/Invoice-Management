from django.contrib import admin
from .models import Customer_User, Customer_User_Push_Notification_Tokens

#add database tables to admin user area here
admin.site.register(Customer_User)
admin.site.register(Customer_User_Push_Notification_Tokens)
