from django.urls import path
from . import views

urlpatterns = [
    path('', views.Search_Submit_View.as_view(), name='search'),
]
