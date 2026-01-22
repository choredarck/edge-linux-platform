import os, json, time
import pymysql
from paho.mqtt import client as mqtt

MQTT_HOST = os.getenv("MQTT_HOST", "mqtt-broker")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER", "edge")
MQTT_PASS = os.getenv("MQTT_PASS", "edgepass")
MQTT_IN_TOPIC = os.getenv("MQTT_IN_TOPIC", "edge/in/#")

DB_HOST = os.getenv("DB_HOST", "mariadb")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "edge_gateway")
DB_USER = os.getenv("DB_USER", "edge")
DB_PASS = os.getenv("DB_PASS", "edgepass")

def db_conn():
    return pymysql.connect(
        host=DB_HOST, port=DB_PORT,
        user=DB_USER, password=DB_PASS,
        database=DB_NAME,
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )

def insert_event(topic: str, payload_bytes: bytes):
    payload_text = payload_bytes.decode("utf-8", errors="replace")

    is_valid = True
    error_reason = None
    payload_json = None

    try:
        payload_json = json.loads(payload_text)
    except Exception:
        # Not JSON — store as JSON object with raw text
        payload_json = {"raw": payload_text}
        is_valid = False
        error_reason = "non-json-payload"

    sql = """
    INSERT INTO ingest_events (src_topic, payload_json, is_valid, error_reason)
    VALUES (%s, %s, %s, %s)
    """

    conn = db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (topic, json.dumps(payload_json), is_valid, error_reason))
    finally:
        conn.close()

def on_connect(client, userdata, flags, rc, props=None):
    print(f"[mqtt] connected rc={rc}")
    client.subscribe(MQTT_IN_TOPIC)
    print(f"[mqtt] subscribed to {MQTT_IN_TOPIC}")

def on_message(client, userdata, msg):
    try:
        insert_event(msg.topic, msg.payload)
        print(f"[db] inserted topic={msg.topic} len={len(msg.payload)}")
    except Exception as e:
        print(f"[error] insert failed: {e}")

def main():
    # Wait a bit for DB readiness (compose health already helps, but keep it robust)
    time.sleep(2)

    c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    c.username_pw_set(MQTT_USER, MQTT_PASS)
    c.on_connect = on_connect
    c.on_message = on_message

    print(f"[mqtt] connecting {MQTT_HOST}:{MQTT_PORT} as {MQTT_USER}")
    c.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    c.loop_forever()

if __name__ == "__main__":
    main()
