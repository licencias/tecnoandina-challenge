# Codigo para publicador
import paho.mqtt.client as mqtt
import time
import datetime
import random
import json

def main():
    while True:
        try:
            datetime_object = str(datetime.datetime.now())

            response = {
                "time": datetime_object,
                "value": round(random.uniform(0, 100), 2),
                "version": random.randint(1, 2)
            }

            client = mqtt.Client()
            client.connect("127.0.0.1", 3001, 60)
            client.publish("challenge/dispositivo/rx", json.dumps(response))

            print(response)

        except Exception as e:
            print(e)

        time.sleep(2)

main()
