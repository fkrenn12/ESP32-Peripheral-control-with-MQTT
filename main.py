import network
import machine
from umqtt.simple import MQTTClient
import time
from adc import get_address
from gpio import execute
from gpio import rgb
from random import randint
import gc

machine.freq(160000000)  # max frequency for ESP32-C6
# General
CLIENT_ADDRESS = get_address()

# WiFi-Konfiguration
SSID = "LAWIG14-FlexBox"
PASSWORD = "wiesengrund14"

# MQTT-Konfiguration
MQTT_BROKER = "192.168.0.93"  # IP-Adresse oder Domain des MQTT-Brokers
MQTT_PORT = 8883
MQTT_SSL = True
MQTT_USER = "admin"  # Benutzername für MQTT-Auth
MQTT_PASSWORD = "admin"  # Passwort für MQTT-Auth

MQTT_CLIENT_ID = f"ESP32-C6-Client_{randint(1, 1000000)}"
MQTT_TOPIC_ROOT_IN = "to-client"
MQTT_TOPIC_ROOT_OUT = "from-client"
print(f'Client Address: {CLIENT_ADDRESS}')
print(f'MQTT Client-ID: {MQTT_CLIENT_ID}')


def connect_mqtt():
    try:
        print(f"Connect to MQTT-Broker {MQTT_BROKER}:{MQTT_PORT}...")
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, ssl=MQTT_SSL, port=MQTT_PORT, user=MQTT_USER,
                            password=MQTT_PASSWORD)
        client.connect()
        print(f"Connected to {MQTT_BROKER}:{MQTT_PORT}")
        return client
    except Exception as e:
        print(f"MQTT-Broker {MQTT_BROKER}:{MQTT_PORT} Connection failed: {e}")
        return None


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)  # WLAN-Interface im Station-Modus
    wlan.active(False)
    time.sleep(0.5)
    wlan.active(True)
    if not wlan.isconnected():  # Prüfen ob bereits verbunden
        print(f"Connect to WiFi {SSID}...")
        wlan.connect(SSID, PASSWORD)
        retries = 0
        while not wlan.isconnected():  # Warten, bis Verbindung hergestellt wird
            retries += 1
            print(retries)
            if retries >= 20:  # Abbruch nach 20 Versuchen (~20 Sekunden)
                print("Connection failed.")
                return False
            rgb[0] = (0, 20, 0)
            rgb.write()
            time.sleep(0.1)
            rgb[0] = (0, 0, 0)
            rgb.write()
            time.sleep(0.9)

    print(f"Connected! IP-Address: {wlan.ifconfig()[0]}")
    return True


def handle_mqtt(topic, msg) -> str | None:
    try:
        topic = topic.replace(f"{MQTT_TOPIC_ROOT_IN}/{CLIENT_ADDRESS}/", "")
        topic_count = len(topic.split("/"))
        freq = None
        direction = None
        if topic_count == 3 and "pwm" in topic:
            typ, pin, freq = topic.split("/")[-3:]
        elif topic_count == 3 and "gpio" in topic:
            typ, pin, direction = topic.split("/")[-3:]
        elif topic_count == 2 and ("adc" in topic or "gpio" in topic):
            typ, pin = topic.split("/")[-2:]
        elif "uart" in topic:
            typ = topic.split("/")[-1]
            pin = None
        else:
            raise Exception('Invalid Topic')
        # print(f"Pin: {pin}, Typ: {typ}, Direction: {direction}, Freq: {freq}, Value: {msg}")
        return execute(pin=pin, typ=typ, value=msg, direction=direction, freq=freq)

    except Exception as e:
        return None
        # return f"Handle MQTT{e}"


def main():
    def mqtt_callback(topic, msg):
        gc.collect()
        rgb[0] = (0, 0, 20)
        rgb.write()
        try:
            topic = topic.decode()
            print(f"Received: {topic} -> {msg.decode()}")
            response = handle_mqtt(topic, msg.decode())
            # print(f"Response: {response} Type: {type(response)}")
            if response is not None:
                topic = topic.replace(MQTT_TOPIC_ROOT_IN, MQTT_TOPIC_ROOT_OUT)
                topic = topic.replace("/?", "")
                mqtt_client.publish(topic, response)
                print(f"Sent: {topic} -> {response}")
        finally:
            rgb[0] = (0, 0, 0)
            rgb.write()

    # Versuchen, eine Verbindung aufzubauen
    if not connect_wifi():
        print("Wifi connection not possible. Restart...")
        machine.reset()  # Neustart bei Verbindungsproblemen

    mqtt_client = connect_mqtt()
    if not mqtt_client:
        print("Connection to MQTT-Broker not possible. Restart...")
        machine.reset()

    rgb[0] = (20, 0, 0)
    rgb.write()
    mqtt_client.set_callback(mqtt_callback)
    subscribe_topic = f"{MQTT_TOPIC_ROOT_IN}/{CLIENT_ADDRESS}/gpio/#"
    print(f"Subscribed to: {subscribe_topic}")
    mqtt_client.subscribe(subscribe_topic.encode())
    subscribe_topic = f"{MQTT_TOPIC_ROOT_IN}/{CLIENT_ADDRESS}/adc/#"
    print(f"Subscribed to: {subscribe_topic}")
    mqtt_client.subscribe(subscribe_topic.encode())
    subscribe_topic = f"{MQTT_TOPIC_ROOT_IN}/{CLIENT_ADDRESS}/pwm/#"
    print(f"Subscribed to: {subscribe_topic}")
    mqtt_client.subscribe(subscribe_topic.encode())
    subscribe_topic = f"{MQTT_TOPIC_ROOT_IN}/{CLIENT_ADDRESS}/uart/#"
    print(f"Subscribed to: {subscribe_topic}")
    mqtt_client.subscribe(subscribe_topic.encode())
    rgb[0] = (0, 0, 0)
    rgb.write()
    counter = 0
    LOOP_DELAY = 0.0015  # should NOT be below 0.0015
    while True:
        try:
            counter += 1
            if counter % (60 // LOOP_DELAY) == 0:  # every minute
                mqtt_client.ping()
                continue

            mqtt_client.check_msg()

            if counter % (1 // LOOP_DELAY) == 0:  # every second
                rgb[0] = (5, 0, 0)
                rgb.write()

            time.sleep(LOOP_DELAY)
            rgb[0] = (0, 0, 0)
            rgb.write()

        except Exception as e:
            print(f"Error: {e}")
            machine.reset()


if __name__ == "__main__":
    main()
