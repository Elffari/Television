import ssl
import time
from . import config
from .device import Device

from paho.mqtt.client import Client, CallbackAPIVersion
from urllib.parse import urlparse

mqtt_client = Client(CallbackAPIVersion.VERSION2)
device = Device(mqtt_client)

def on_connect(mqtt, obj, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected [secure]")
        mqtt.subscribe("downlink/#", qos=0)
        device.connected()
    elif reason_code == "Bad user name or password":
        print("Invalid BLYNK_AUTH_TOKEN")
        mqtt.disconnect()
    else:
        raise Exception(f"MQTT connection error: {reason_code}")

def on_message(mqtt, obj, msg):
    payload = msg.payload.decode("utf-8")
    topic = msg.topic
    if topic == "downlink/redirect":
        url = urlparse(payload)
        print("Redirecting...")
        mqtt.connect_async(url.hostname, url.port, 45)
    elif topic == "downlink/reboot":
        print("Reboot command received!")
    elif topic == "downlink/ping":
        pass # MQTT client library automatically sends the QOS1 response
    elif topic == "downlink/diag":
        print("Server says:", payload)
    else:
        print(f"Got {topic}, value: {payload}")
        device.process_message(topic, payload)

def main():
    mqtt_client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.username_pw_set("device", config.BLYNK_AUTH_TOKEN)
    mqtt_client.connect_async(config.BLYNK_MQTT_BROKER, 8883, 45)
    mqtt_client.loop_start()

    while True:
        device.update()
        time.sleep(1)

if __name__ == "__main__":
    main()
