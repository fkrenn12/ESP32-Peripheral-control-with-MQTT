import paho.mqtt.client as mqtt
import time
import random
import json
from collections import deque

broker = '192.168.0.93'
port = 8883
topic = "to-client/54/uart"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
#pattern = [1, 0b11000011, 0b11001100, 0b11110000, 0b11010100, 0b11111111]
pattern = [0b00111101, 0b00111011, 0b00111001,0b00111001, 0b00111001]

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}\n")

    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS, cert_reqs=mqtt.ssl.CERT_NONE)
    # client.username_pw_set(username='wei', password='I9y9t6uEpjJH')
    # client.username_pw_set(username='admin', password='franz_s10rr6fr_246_franz')
    client.username_pw_set(username='admin', password='admin')
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    d = deque(pattern)
    while True:
        time.sleep(0.25)
        d.rotate(1)
        message = json.dumps({"pin": 2, "autoclear": 1,
                              "pattern": [random.randint(1, 255), random.randint(1, 100), random.randint(1, 100),
                                          random.randint(1, 255), random.randint(1, 100), random.randint(1, 100)],
                              "repeat": 0})
        message = json.dumps(
            {"pin": 2, "autoclear": 1, "pattern": list(d),
             "repeat": 0})

        result = client.publish('to-client/54/uart', message, qos=0)
        status = result[0]
        if status == 0:
            print(f"Send `{message}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
