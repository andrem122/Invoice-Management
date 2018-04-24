from django.urls import path
from . import views

urlpatterns = [
    path('', views.Search_Submit_View.as_view(), name='search'),
    path('ajax', views.Search_Ajax_Submit_View.as_view(), name='search-ajax'),
]
