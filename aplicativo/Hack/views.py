# Hack/views.py
from django.shortcuts import render
from .models import Sensor

def sensor_data_view(request):
    sensores = Sensor.objects.all().order_by('-data_hora')
    return render(request, 'sensor_data.html', {'sensores': sensores})
