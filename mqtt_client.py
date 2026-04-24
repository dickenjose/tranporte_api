import json
import paho.mqtt.client as mqtt
from services.pago_service import procesar_pago

BROKER = "72.61.34.39"
PORT = 1883


# ✅ FIX: agregar properties=None (OBLIGATORIO en MQTT v2)
def on_connect(client, userdata, flags, rc, properties=None):
    print("✅ Conectado a HiveMQ público con código:", rc)
    #client.subscribe("ana123/bus/001/pago")
    client.subscribe("esp32/pago")


def on_message(client, userdata, msg):
    try:
        print("\n==============================")
        print("📩 MENSAJE RECIBIDO")
        print("==============================")

        print("📡 Topic:", msg.topic)
        print("📦 Payload RAW:", msg.payload)
        print("🔤 Payload decodificado:", msg.payload.decode())

        # Intentar convertir a JSON
        try:
            data = json.loads(msg.payload.decode())
            print("📊 JSON:", data)
        except:
            print("⚠️ No es JSON válido")

        # EXTRAER DATOS
        bus_id = msg.topic.split("/")[1] if "/" in msg.topic else "N/A"

        if 'data' in locals():
            uid = data.get("uid")
            tipo_tarifa = data.get("tipo_tarifa") or data.get("tipo")

            print("🆔 UID:", uid)
            print("💰 Tipo tarifa:", tipo_tarifa)

            respuesta = procesar_pago(uid, tipo_tarifa, bus_id)

            topic_respuesta = "esp32/respuesta"
            client.publish(topic_respuesta, json.dumps(respuesta))

            print("📤 Respuesta enviada:", respuesta)

        print("==============================\n")

    except Exception as e:
        print("❌ Error procesando mensaje:", e)



# ✅ FIX: usar versión correcta del API MQTT v2
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

print("🔥 Escuchando en broker público...")
client.loop_forever()
