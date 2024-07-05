# Hack/models.py
from django.db import models

class Sensor(models.Model):
    id_sensor = models.IntegerField()
    leitura_sensor = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    cep = models.CharField(max_length=9)
    distancia_sensor_solo = models.FloatField()
    status_area = models.CharField(max_length=20)
    data_hora = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Sensor {self.id_sensor} - {self.leitura_sensor}"
