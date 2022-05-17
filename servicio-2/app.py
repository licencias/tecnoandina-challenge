# Codigo para subscriptor
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from datetime import datetime
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "my-admin-token"
org = "tecnoandina"
bucket = "system"
url = "http://influx:8086"

def send_data_influx_db(json_payload):
    with InfluxDBClient(url=url, token=token, org=org) as client:   
        payload = json.loads(json_payload)
        # senddata={}
        # senddata["measurement"] = "test06"
        # senddata["measurement"] = "test06"
        # senddata["tags"] = {}
        # senddata["tags"]["version"] = payload['version']
        # senddata["fields"]={}
        # senddata["fields"]["time"] = payload['time']
        # senddata["fields"]["value"] = str(payload['value'])
        point = Point("Test06") \
            .tag("version", payload['version']) \
            .field("time", payload['time']) \
            .field("value", payload['value'])

        print("data", point)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, record=point)

def on_connect(client, userdata, flags, rc):
    print("Se conecto con mqtt " + str(rc))
    client.subscribe("challenge/dispositivo/#")
    pass


def on_message(client, userdata, msg):
    if msg.topic == "challenge/dispositivo/rx":
        print(msg.payload)
        send_data_influx_db(msg.payload)
    pass


def main():
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("mosquitto", 1883)
        client.loop_forever()
    except Exception as e:
        print(e)


main()
