from random import randint

import paho.mqtt.client as mqtt
import time
import random
import json
from collections import deque

TOENE_HZ = [440,460,480,500,520,540,560,580,600,620]
broker = '10.96.39.181'
port = 1883
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def on_message(client, userdata, message):
    print(f"Received `{str(message.payload.decode())}` from `{message.topic}` topic")


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe("from-client/#")
        else:
            print(f"Failed to connect, return code {rc}\n")

    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    # client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS, cert_reqs=mqtt.ssl.CERT_NONE)
    # client.username_pw_set(username='', password='')
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    message = json.dumps({"animation": 1})
    client.publish('to-client/11/uart', message, qos=0)
    message = json.dumps({"strips": [2, 3], "pixels": 8, "pattern": [1, 2, 3, 7, 11, 7, 2, 1], "repeat": 0, "animation-mode":
        "rotate-right", "interval": 100})
    client.publish('to-client/11/uart', message, qos=0)
    message = json.dumps({"strip": 3, "pixels": 8, "pattern": [16], "repeat": 1, "animation-mode":
        "rotate-left", "interval": 50})
    client.publish('to-client/11/uart', message, qos=0)

    client.publish('to-client/11/pwm/22/5', 50, qos=0)  # 5Hz - 50%
    client.publish('to-client/11/pwm/21/2', 5, qos=0)  # 2Hz - 5%
    client.publish('to-client/15/pwm/22/100', 5, qos=0)  # 100Hz - 5%
    client.publish('to-client/55/pwm/22/5', 50, qos=0)  # 5Hz - 50%
    client.publish('to-client/55/pwm/21/2000', 50, qos=0)  # 5Hz - 50%
    while True:
        time.sleep(1)
        message = json.dumps({"strip": 1, "pixels": 2, "pattern": [randint(0, 10), randint(11, 29)], "repeat": 1})
        client.publish('to-client/11/uart', message, qos=0)
        message = 0
        result = client.publish('to-client/11/adc/2', message, qos=0)
        result = client.publish('to-client/15/adc/2', message, qos=0)
        result = client.publish('to-client/55/adc/2', message, qos=0)
        client.publish(f'to-client/55/pwm/21/{TOENE_HZ[randint(0, len(TOENE_HZ)-1)]}', 50, qos=0)  # 5Hz - 50%
        message = randint(20, 75)
        client.publish('to-client/15/pwm/21/300', message, qos=0)
        status = result[0]
        if status != 0:
            print(f"Failed to send message to topic")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.on_message = on_message
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
