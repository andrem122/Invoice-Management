from django.urls import path
from . import views

app_name = 'search_submit'

urlpatterns = [
    path('', views.Search_Submit_View.as_view(), name='search'),
    path('ajax', views.Search_Submit_Ajax_View.as_view(), name='search-ajax'),
]
