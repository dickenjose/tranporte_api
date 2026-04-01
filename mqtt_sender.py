import json
import time
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883

TOPIC_PAGO = "ana123/bus/001/pago"
TOPIC_RESPUESTA = "ana123/bus/001/respuesta"


# ✅ cuando conecta
def on_connect(client, userdata, flags, rc, properties=None):
    print("✅ Conectado al broker")

    # 🔥 IMPORTANTE: suscribirse a la respuesta
    client.subscribe(TOPIC_RESPUESTA)


# 📩 recibir mensajes
def on_message(client, userdata, msg):
    print("\n📩 Respuesta recibida:")
    print(msg.topic, msg.payload.decode())


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

client.loop_start()

time.sleep(1)

# 📤 enviar pago
data = {
    "uid": "ABCDEF12",
    "tipo_tarifa": "estudiante"
}

client.publish(TOPIC_PAGO, json.dumps(data))

print("📤 Mensaje enviado:", data)

# ⏳ esperar respuesta
time.sleep(5)

client.loop_stop()
client.disconnect()
