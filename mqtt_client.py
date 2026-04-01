import json
import paho.mqtt.client as mqtt
from services.pago_service import procesar_pago

BROKER = "test.mosquitto.org"
PORT = 1883


# ✅ FIX: agregar properties=None (OBLIGATORIO en MQTT v2)
def on_connect(client, userdata, flags, rc, properties=None):
    print("✅ Conectado a HiveMQ público con código:", rc)
    client.subscribe("ana123/bus/001/pago")


def on_message(client, userdata, msg):
    try:
        print("\n📩 Mensaje recibido:", msg.topic)

        bus_id = msg.topic.split("/")[1]

        data = json.loads(msg.payload.decode())

        uid = data.get("uid")
        tipo_tarifa = data.get("tipo_tarifa")

        respuesta = procesar_pago(uid, tipo_tarifa, bus_id)

        topic_respuesta = f"ana123/bus/001/respuesta"
        client.publish(topic_respuesta, json.dumps(respuesta))

        print("📤 Respuesta enviada:", respuesta)

    except Exception as e:
        print("❌ Error procesando mensaje:", e)


# ✅ FIX: usar versión correcta del API MQTT v2
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

print("🔥 Escuchando en broker público...")
client.loop_forever()
