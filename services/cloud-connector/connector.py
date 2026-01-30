import os
import time
from paho.mqtt import client as mqtt

EDGE_HOST = os.getenv("EDGE_MQTT_HOST", "mqtt-broker")
EDGE_PORT = int(os.getenv("EDGE_MQTT_PORT", "1883"))
EDGE_USER = os.getenv("EDGE_MQTT_USER", "")
EDGE_PASS = os.getenv("EDGE_MQTT_PASS", "")
EDGE_TOPIC = os.getenv("EDGE_TOPIC", "edge/internal/events")

CLOUD_HOST = os.getenv("CLOUD_MQTT_HOST")
CLOUD_PORT = int(os.getenv("CLOUD_MQTT_PORT", "8883"))
CLOUD_USER = os.getenv("CLOUD_MQTT_USER")
CLOUD_PASS = os.getenv("CLOUD_MQTT_PASS")
CLOUD_TOPIC = os.getenv("CLOUD_TOPIC", "edge/cloud/events")
CLOUD_TLS  = os.getenv("CLOUD_TLS", "true").lower() == "true"

if not CLOUD_HOST or not CLOUD_USER or not CLOUD_PASS:
    raise SystemExit("Missing CLOUD_MQTT_HOST / CLOUD_MQTT_USER / CLOUD_MQTT_PASS")

cloud = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
cloud.username_pw_set(CLOUD_USER, CLOUD_PASS)
if CLOUD_TLS:
    cloud.tls_set()
    cloud.tls_insecure_set(False)

edge = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
if EDGE_USER:
    edge.username_pw_set(EDGE_USER, EDGE_PASS)

def on_cloud_connect(c, *_):
    print("[cloud] connected")

def on_edge_connect(c, *_):
    print(f"[edge] connected; subscribe {EDGE_TOPIC}")
    c.subscribe(EDGE_TOPIC, qos=1)

def on_edge_message(c, userdata, msg):
    try:
        r = cloud.publish(CLOUD_TOPIC, msg.payload, qos=1)
        if r.rc != 0:
            print(f"[cloud] publish rc={r.rc}")
        else:
            print(f"[bridge] {msg.topic} -> {CLOUD_TOPIC} bytes={len(msg.payload)}")
    except Exception as e:
        print(f"[error] publish failed: {e}")

def main():
    cloud.on_connect = on_cloud_connect
    edge.on_connect = on_edge_connect
    edge.on_message = on_edge_message

    print(f"[cloud] connect {CLOUD_HOST}:{CLOUD_PORT} tls={CLOUD_TLS}")
    cloud.connect(CLOUD_HOST, CLOUD_PORT, keepalive=60)
    cloud.loop_start()

    time.sleep(1)

    print(f"[edge] connect {EDGE_HOST}:{EDGE_PORT}")
    edge.connect(EDGE_HOST, EDGE_PORT, keepalive=60)
    edge.loop_forever()

if __name__ == "__main__":
    main()
