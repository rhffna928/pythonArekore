import paho.mqtt.client as mqtt
import json

BROKER = "mqtt-broker-service"
PORT = 1883
TOPICS = ["sensor/data", "device/status", "alerts"]

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    for topic in TOPICS:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    topic = msg.topic
    
    # 메시지 토픽에 따라 다른 서비스로 전달
    if topic == "sensor/data":
        forward_message("forwarder-service", payload)
    elif topic == "device/status":
        forward_message("db-writer-service", payload)
    elif topic == "alerts":
        forward_message("alert-service", payload)

def forward_message(service, message):
    print(f"Forwarding message to {service}: {message}")
    # HTTP API 또는 다른 메시징 시스템으로 전달 가능

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_forever()
