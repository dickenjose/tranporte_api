from config.database import micros, usuarios
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime


# 🔹 CREAR MICRO
def crear_micro(data):
    # 🔍 validar placa única
    if micros.find_one({"placa": data.placa}):
        raise HTTPException(400, "La placa ya existe")

    # 🔍 validar chofer (si viene)
    if data.chofer_id:
        chofer = usuarios.find_one({"_id": ObjectId(data.chofer_id)})

        if not chofer:
            raise HTTPException(404, "Chofer no existe")

        if "roles" not in chofer or "chofer" not in chofer["roles"]:
            raise HTTPException(400, "El usuario no es chofer")

    nuevo = {
        "nombre": data.nombre,
        "placa": data.placa,
        "chofer_id": data.chofer_id,
        "linea": getattr(data, "linea", None),

        # 🔥 preparado para RFID
        "dispositivos": [],

        "estado": data.estado or "activo",
        "fecha_registro": datetime.utcnow(),
        "fecha_actualizacion": None
    }

    result = micros.insert_one(nuevo)

    return {
        "ok": True,
        "id": str(result.inserted_id)
    }


# 🔹 LISTAR MICROS
def listar_micros():
    lista = []

    for m in micros.find():
        m["id"] = str(m["_id"])
        del m["_id"]

        # 🔥 opcional: traer nombre del chofer
        if m.get("chofer_id"):
            try:
                chofer = usuarios.find_one({"_id": ObjectId(m["chofer_id"])})
                if chofer:
                    m["chofer_nombre"] = chofer.get("nombre")
            except:
                m["chofer_nombre"] = None

        lista.append(m)

    return lista


# 🔹 OBTENER MICRO
def obtener_micro(micro_id):
    micro = micros.find_one({"_id": ObjectId(micro_id)})

    if not micro:
        raise HTTPException(404, "Micro no encontrado")

    micro["id"] = str(micro["_id"])
    del micro["_id"]

    # 🔥 traer nombre del chofer
    if micro.get("chofer_id"):
        chofer = usuarios.find_one({"_id": ObjectId(micro["chofer_id"])})
        if chofer:
            micro["chofer_nombre"] = chofer.get("nombre")

    return micro


# 🔹 ACTUALIZAR MICRO
def actualizar_micro(micro_id, data):
    micro = micros.find_one({"_id": ObjectId(micro_id)})

    if not micro:
        raise HTTPException(404, "Micro no encontrado")

    update_data = {k: v for k, v in data.dict().items() if v is not None}

    # 🔍 validar placa única
    if "placa" in update_data and update_data["placa"] != micro["placa"]:
        if micros.find_one({"placa": update_data["placa"]}):
            raise HTTPException(400, "La placa ya existe")

    # 🔍 validar chofer
    if "chofer_id" in update_data:
        if update_data["chofer_id"] is not None:
            chofer = usuarios.find_one({"_id": ObjectId(update_data["chofer_id"])})

            if not chofer:
                raise HTTPException(404, "Chofer no existe")

            if "roles" not in chofer or "chofer" not in chofer["roles"]:
                raise HTTPException(400, "El usuario no es chofer")

    update_data["fecha_actualizacion"] = datetime.utcnow()

    micros.update_one(
        {"_id": ObjectId(micro_id)},
        {"$set": update_data}
    )

    return {"ok": True}


# 🔹 ELIMINAR MICRO
def eliminar_micro(micro_id):
    result = micros.delete_one({"_id": ObjectId(micro_id)})

    if result.deleted_count == 0:
        raise HTTPException(404, "Micro no encontrado")

    return {"ok": True}


# 🔹 ASIGNAR DISPOSITIVO A MICRO
def asignar_dispositivo(micro_id, device_id):
    micro = micros.find_one({"_id": ObjectId(micro_id)})

    if not micro:
        raise HTTPException(404, "Micro no encontrado")

    dispositivos = micro.get("dispositivos", [])

    if device_id in dispositivos:
        raise HTTPException(400, "El dispositivo ya está asignado")

    dispositivos.append(device_id)

    micros.update_one(
        {"_id": ObjectId(micro_id)},
        {"$set": {
            "dispositivos": dispositivos,
            "fecha_actualizacion": datetime.utcnow()
        }}
    )

    return {"ok": True}


# 🔹 QUITAR DISPOSITIVO
def quitar_dispositivo(micro_id, device_id):
    micro = micros.find_one({"_id": ObjectId(micro_id)})

    if not micro:
        raise HTTPException(404, "Micro no encontrado")

    dispositivos = micro.get("dispositivos", [])

    if device_id not in dispositivos:
        raise HTTPException(404, "Dispositivo no está en el micro")

    dispositivos.remove(device_id)

    micros.update_one(
        {"_id": ObjectId(micro_id)},
        {"$set": {
            "dispositivos": dispositivos,
            "fecha_actualizacion": datetime.utcnow()
        }}
    )

    return {"ok": True}