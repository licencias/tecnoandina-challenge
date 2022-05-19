# Codigo para publicador
import paho.mqtt.client as mqtt
import time
import datetime
import random
import json


def main():
    try:
        client = mqtt.Client()
        client.connect("mosquitto", 1883, 60)

        while True:

            response = check_device()

            client.publish("challenge/dispositivo/rx",
                           json.dumps(response))

            print(response)
            time.sleep(60)

    except Exception as e:
        print(e)


def check_device():

    datetime_object = str(datetime.datetime.now())

    response = {
        "time": datetime_object,
        "value": round(random.uniform(0, 1000), 2),
        "version": random.randint(1, 2)
    }

    return response


main()
