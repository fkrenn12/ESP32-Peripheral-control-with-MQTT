import paho.mqtt.client as mqtt
import time
import random
import json
from collections import deque

broker = '192.168.0.93'
port = 8883
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
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS, cert_reqs=mqtt.ssl.CERT_NONE)
    client.username_pw_set(username='admin', password='admin')
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    message = 50
    client.publish('to-client/11/pwm/22/5', message, qos=0)

    message = 5
    client.publish('to-client/11/pwm/21/2', message, qos=0)

    message = 50
    client.publish('to-client/15/pwm/22/10', message, qos=0)

    message = 50
    client.publish('to-client/55/pwm/22/5', message, qos=0)
    while True:
        time.sleep(1)
        message = json.dumps({"strip": 1, "pixels": 2, "pattern": [1, 2], "repeat": 1})
        client.publish('to-client/11/uart', message, qos=0)
        message = 0
        result = client.publish('to-client/11/adc/2', message, qos=0)
        result = client.publish('to-client/15/adc/2', message, qos=0)
        result = client.publish('to-client/55/adc/2', message, qos=0)
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
