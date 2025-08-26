import asyncio
import time
import json
import random

from gmqtt import Client as MQTTClient
from gmqtt.mqtt.constants import MQTTv311

STOP = asyncio.Event()

previous_time = time.time()


def on_connect(client, flags, rc, properties):
    print('Connected')
    client.subscribe('wei/#', qos=0)


def on_message(client, topic, payload, qos, properties):
    global previous_time
    if payload:
        print(f'RECV MSG: {time.time() - previous_time} {payload}')
        previous_time = time.time()


def on_disconnect(client, packet, exc=None):
    print('Disconnected')


def on_subscribe(client, mid, qos, properties):
    print('SUBSCRIBED')


async def main():
    client = MQTTClient("client-iwewevvd")

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe
    # client.set_auth_credentials(username='wei', password='I9y9t6uEpjJH')
    # await asyncio.wait_for(client.connect(host="mqtt.htl-hl.ac.at", port=8883, ssl=bool(1)), 10)
    client.set_auth_credentials(username='admin', password='admin')
    await asyncio.wait_for(client.connect(host="192.168.0.93", port=1883, ssl=bool(0)), 10)
    # client.set_auth_credentials(username='wei', password='I9y9t6uEpjJH')
    # await asyncio.wait_for(client.connect(host="mqtt.htl-hl.ac.at", port=8883, ssl=bool(1)), 10)
    # client.set_auth_credentials(username='admin', password='franz_s10rr6fr_246_franz')
    # await asyncio.wait_for(client.connect(host="techfit.at", port=8883, version=MQTTv311, ssl=True), 10)

    while True:
        await asyncio.sleep(1)
        message = json.dumps({"pin": 2, "autoclear": 1,
                              "pattern": [random.randint(1, 255), random.randint(1, 100), random.randint(1, 100)],
                              "repeat": 0})
        #message = json.dumps(
        #    {"pin": 2, "autoclear": 1, "pattern": [1,2,3,4,5,6],
        #     "repeat": 0})

        # client.publish('wei/to-client/54/uart', message, qos=2)
        # print(message)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
