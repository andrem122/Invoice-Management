from django.urls import path
from . import views

urlpatterns = [
    path('<int:house_id>', views.project_details, name='project_details'),
]
