#Codigo para publicador
import paho.mqtt.client as mqtt
import time
import datetime
import random
import json

def main():
    while True:
      datetime_object = str(datetime.datetime.now())

      response = {
          "time": datetime_object,
          "value": round(random.uniform(0, 100), 2),
          "version": random.randint(1, 2)
      }

      client = mqtt.Client()
      client.connect("127.0.0.1", 1883, 60)
      client.publish("challenge/dispositivo/rx", json.dumps(response))

      time.sleep(60)

main()