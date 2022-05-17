# Codigo para subscriptor
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from datetime import datetime
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb import InfluxDBClient
#from influxdb_client.client.write_api import SYNCHRONOUS

token = "my-token"
org = "tecnoandina"
bucket = "system"

# #Setup database
# client = InfluxDBClient('localhost', 8086, 'admin', 'admin', 'mydb')
# client.create_database('mydb')
# client.get_list_database()
# client.switch_database('mydb')


def send_data_influx_db(json_payload):
    # with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
    client = InfluxDBClient('influx', '8086', 'admin', 'admin', 'system')
 
    #client.create_database('system')
    # print("parte2")
    #client.get_list_database()
    # print("parte3")
    #client.switch_database('system')
    # print("parte4")
    # #write_api = client.write_api(write_options=SYNCHRONOUS)

    payload = json.loads(json_payload)
    # print("parte5")

    # point = Point("Test04") \
    #     .tag("version", payload['version']) \
    #     .field("time", payload['time']) \
    #     .field("value", str(payload['value']))
    
    # print("parte6")

    # print("data", point)
    # write_api.write(bucket, org, point)

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
