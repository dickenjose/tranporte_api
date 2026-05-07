from config.database import db, usuarios, micros
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime


# 🔥 colección devices
devices = db.devices


# -----------------------------
# ➕ CREAR DEVICE
# -----------------------------
def crear_device(data):
    # validar duplicado
    if devices.find_one({"device_id": data.device_id}):
        raise HTTPException(400, "Device ya existe")

    micro = None

    # validar micro si viene
    if data.micro_id:
        micro = micros.find_one({"_id": ObjectId(data.micro_id)})
        if not micro:
            raise HTTPException(404, "Micro no encontrado")

    nuevo = {
        "device_id": data.device_id,
        "micro_id": data.micro_id,
        "estado": data.estado or "activo",
        "firmware_version": data.firmware_version,
        "wifi_ssid": data.wifi_ssid,
        "fecha_registro": datetime.utcnow(),
        "ultima_conexion": None,
        "topic": None
    }

    result = devices.insert_one(nuevo)
    device_id = str(result.inserted_id)

    # 🔥 generar topic MQTT si tiene micro
    if data.micro_id:
        topic = f"micro/{data.micro_id}/device/{data.device_id}/rfid"
        devices.update_one(
            {"_id": ObjectId(device_id)},
            {"$set": {"topic": topic}}
        )

    return device_id


# -----------------------------
# 📋 LISTAR DEVICES
# -----------------------------
def listar_devices():
    return list(devices.find())


# -----------------------------
# 🔍 OBTENER DEVICE
# -----------------------------
def obtener_device(device_id):
    device = devices.find_one({"_id": ObjectId(device_id)})

    if not device:
        raise HTTPException(404, "Device no encontrado")

    return device


# -----------------------------
# ✏️ ACTUALIZAR DEVICE
# -----------------------------
def actualizar_device(device_id, data):
    device = obtener_device(device_id)

    update_data = {k: v for k, v in data.dict().items() if v is not None}

    # validar micro si se cambia
    if "micro_id" in update_data:
        micro = micros.find_one({"_id": ObjectId(update_data["micro_id"])})
        if not micro:
            raise HTTPException(404, "Micro no encontrado")

        # regenerar topic MQTT
        update_data["topic"] = f"micro/{update_data['micro_id']}/device/{device['device_id']}/rfid"

    devices.update_one(
        {"_id": ObjectId(device_id)},
        {"$set": update_data}
    )


# -----------------------------
# ❌ ELIMINAR DEVICE
# -----------------------------
def eliminar_device(device_id):
    result = devices.delete_one({"_id": ObjectId(device_id)})

    if result.deleted_count == 0:
        raise HTTPException(404, "Device no encontrado")


# -----------------------------
# 🔗 ASIGNAR DEVICE A MICRO
# -----------------------------
def asignar_device_micro(device_id, micro_id):
    device = obtener_device(device_id)

    micro = micros.find_one({"_id": ObjectId(micro_id)})
    if not micro:
        raise HTTPException(404, "Micro no encontrado")

    topic = f"micro/{micro_id}/device/{device['device_id']}/rfid"

    devices.update_one(
        {"_id": ObjectId(device_id)},
        {
            "$set": {
                "micro_id": micro_id,
                "topic": topic
            }
        }
    )


# -----------------------------
# 🔓 DESASIGNAR DEVICE
# -----------------------------
def quitar_device_micro(device_id):
    obtener_device(device_id)

    devices.update_one(
        {"_id": ObjectId(device_id)},
        {
            "$set": {
                "micro_id": None,
                "topic": None
            }
        }
    )