from django.urls import path
from . import views

urlpatterns = [
    #example: site/job
    path('', views.index, name='index'),
    path('redirect', views.redirect_user, name='redirect_user'),
    path('<int:job_id>', views.job_detail, name='job_detail'),
]
