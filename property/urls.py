from django.urls import path
from .views import PropertyCreateView

app_name = 'property'

urlpatterns = [
    path('add-property', PropertyCreateView.as_view(), name='add_property'),
]
