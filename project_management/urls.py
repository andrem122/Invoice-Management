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
    path('admin/', admin.site.urls),
    path('jobs/', include('jobs.urls')),
    path('jobs_admin/', include('jobs_admin.urls')),
    path('addjob/', include('addjob.urls')),
    path('payment_history/', include('payment_history.urls')),
    path('payments/', include('payment_requests.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', include('register.urls')),
    path('customer_register/', include('customer_register.urls')),
    path('jobs_complete/', include('jobs_complete.urls')),
    path('add_house/', include('add_house.urls')),
    path('download_data/', include('download_data.urls')),
    path('projects/', include('projects.urls')),
    path('search/', include('search_submit.urls')),
    path('send_data/', include('send_data.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
