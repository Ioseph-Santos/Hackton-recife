import json
import random
from datetime import datetime
from paho.mqtt import client as mqtt_client
import os
import django

# Configurar as variáveis de ambiente para Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aplicativo.settings')
django.setup()

# Importar o modelo do Django
from Hack.models import Sensor

def load_json_to_dict(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf8') as f:
        data = json.load(f)
    return data
map_dist_sensor = { '1':40.0, '2':80.0}
map_nivel_alerta = {'1':'Nível de alerta 1', '2':'Nível de alerta 2'}
broker = 'beaver.rmq.cloudamqp.com'
port = 1883
topic = "sensor/nivel"
client_id = f'subscribe-{random.randint(0, 100)}'
username = 'apeqbhrd:apeqbhrd'
password = 'K-b29D68bu8rUcgd-8Y35GpsDIGioV8q'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}\n")

    client = mqtt_client.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        msg_payload = str(msg.payload.decode()).split(":")
        sensor = msg_payload[0][-1]
        sensor_value = float(msg_payload[1].strip().replace("'", ''))
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        
        usuario = Sensor(
            id_sensor= sensor, 
            leitura_sensor=sensor_value,
            latitude=123456,  
            longitude=123456,  
            cep='00000-000',  
            distancia_sensor_solo = map_dist_sensor.get(sensor, -1),  
            status_area='OK' if not bool(sensor_value) else map_nivel_alerta.get(sensor,None) 
        )
        usuario.save()
        print(f"{date_time} - sensor {sensor}:{sensor_value} saved to database")
        
    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
