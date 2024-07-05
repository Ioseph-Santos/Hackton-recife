# Hack/urls.py
from django.urls import path
from .views import sensor_data_view

urlpatterns = [
    path('sensores/', sensor_data_view, name='sensor_data'),
]
