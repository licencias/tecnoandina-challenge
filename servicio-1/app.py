# Codigo para publicador
import paho.mqtt.client as mqtt
import time
import datetime
import random
import json


def main():
    try:   
        client = mqtt.Client()
        client.connect("localhost", 1883, 60)
               
        while True:

            datetime_object = str(datetime.datetime.now())

            response = {
                "time": datetime_object,
                "value": round(random.uniform(0, 1000), 2),
                "version": random.randint(1, 2)
            }
            client.publish("challenge/dispositivo/rx",
                           json.dumps(response))

            print(response)
            time.sleep(2)

    except Exception as e:
        print(e)


main()