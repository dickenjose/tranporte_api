import json
import traceback
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883

TOPIC_SUB = "ana123/bus/+/pago"   # 👈 IMPORTANTE


# 🔥 conexión
def on_connect(client, userdata, flags, rc):
    print("🔌 Intentando conectar...")
    print("Código conexión:", rc)

    if rc == 0:
        print("✅ Conectado correctamente al broker")
        client.subscribe(TOPIC_SUB)
        print("📡 Suscrito a:", TOPIC_SUB)
    else:
        print("❌ Error de conexión")


# 🔥 recibir mensajes
def on_message(client, userdata, msg):
    try:
        print("\n📥 MENSAJE RECIBIDO")
        print("Topic:", msg.topic)
        print("Payload RAW:", msg.payload)

        data = json.loads(msg.payload.decode())

        print("📦 JSON:", data)

        # responder (solo prueba)
        response_topic = msg.topic.replace("pago", "respuesta")

        respuesta = {
            "estado": "ok",
            "mensaje": "mensaje recibido correctamente"
        }

        client.publish(response_topic, json.dumps(respuesta))

        print("📤 Respuesta enviada:", respuesta)

    except Exception:
        print("❌ ERROR PROCESANDO MENSAJE")
        traceback.print_exc()


# 🔥 crear cliente
client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message


print("🚀 Iniciando cliente MQTT...")

client.connect(BROKER, PORT)

client.loop_forever()
