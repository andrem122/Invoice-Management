"""project_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('customer_register.urls')),
    path('admin/', admin.site.urls),
    path('jobs/', include('jobs.urls')),
    path('jobs-admin/', include('jobs_admin.urls')),
    path('addjob/', include('addjob.urls')),
    path('payment-history/', include('payment_history.urls')),
    path('payments/', include('payment_requests.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', include('register.urls')),
    path('add-house/', include('add_house.urls')),
    path('add-expense/', include('add_expense.urls')),
    path('expenses/', include('expenses.urls')),
    path('download-data/', include('download_data.urls')),
    path('projects/', include('projects.urls')),
    path('search/', include('search_submit.urls')),
    path('send-data/', include('send_data.urls')),
    path('project-details/', include('project_details.urls')),
    path('customer-payments/', include('customer_payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
