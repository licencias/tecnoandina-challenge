#Codigo para subscriptor
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from datetime import datetime
import json

#Setup database
# client = InfluxDBClient('localhost', 8086, 'admin', 'Password1', 'mydb')
# client.create_database('mydb')
# client.get_list_database()
# client.switch_database('mydb')

def send_data_influx_db(json_payload):
    payload = json.loads(json_payload)
    data = {
        "measurement": "dispositivos",
        "tags": {
            "version": payload['version']
            },
        "fields": {
            'time': payload['time'],
            'value': payload['value']
        }
    }
    print("data",data)

    #json_payload.append(data)

    #Send our payload

    #client.write_points(json_payload)

def on_connect(client, userdata, flags, rc):
    print("Se conecto con mqtt " + str(rc))
    client.subscribe("challenge/dispositivo/#")

def on_message(client, userdata, msg):
    if msg.topic == "challenge/dispositivo/rx":
        print(f"Temperatura es {str(msg.payload)}")
        send_data_influx_db(msg.payload)
    print(msg.topic + " " + str(msg.payload))

def main():
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("localhost", 3001)
        client.loop_forever()
    except Exception as e:
            print(e)

main()