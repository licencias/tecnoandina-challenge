# Codigo para subscriptor
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from datetime import datetime
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "Z3OiLCIbqlNM77hfB5YVZEO8XhAeuIDKl2OlgeYbLR-t48qhFbwHoEmlwB6pp2-F4Tkb-WsZ2Qe7DAzxwW2JpQ=="
org = "tecnoandina"
bucket = "system"

# #Setup database
# client = InfluxDBClient('localhost', 8086, 'admin', 'admin', 'mydb')
# client.create_database('mydb')
# client.get_list_database()
# client.switch_database('mydb')


def send_data_influx_db(json_payload):
    with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)

        payload = json.loads(json_payload)

        # data = {
        #     "measurement": "dispositivos",
        #     "tags": {
        #         "version": payload['version']
        #     },
        #     "fields": {
        #         'time': payload['time'],
        #         'value': str(payload['value'])
        #     }
        # }

        point = Point("Test01") \
            .tag("version", payload['version']) \
            .field("time", payload['time']) \
            .field("value",str(payload['value']))

        print("data", point)
        write_api.write(bucket, org, point)

def on_connect(client, userdata, flags, rc):
    print("Se conecto con mqtt " + str(rc))
    client.subscribe("challenge/dispositivo/#")


def on_message(client, userdata, msg):
    if msg.topic == "challenge/dispositivo/rx":
        print(str(msg.payload))

        #envio mensaje a influx
        send_data_influx_db(msg.payload)
    print(msg.topic + " " + str(msg.payload))


def main():
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("localhost", 1883)
        client.loop_forever()
    except Exception as e:
        print(e)


main()
